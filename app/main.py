# app/main.py
from fastapi import FastAPI, Request, Query, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.utils.logger import get_logger
from app.services import ai, shopify, whatsapp

log = get_logger("app")
app = FastAPI(title="Enterprise AI Automation Agent")

# ----------------------------
# Healthcheck
# ----------------------------
@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENV}

# ----------------------------
# WhatsApp Webhook (GET verify)
# ----------------------------
@app.get("/webhook/whatsapp")
async def verify(
    mode: str | None = Query(None),
    challenge: str | None = Query(None),
    token: str | None = Query(None),
):
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(challenge) if challenge and challenge.isdigit() else (challenge or "OK")
    raise HTTPException(status_code=403, detail="Verification failed")

# ----------------------------
# WhatsApp Webhook (POST receive)
# ----------------------------
@app.post("/webhook/whatsapp")
async def receive(req: Request):
    body = await req.json()
    log.info(f"WA webhook: {str(body)[:500]}")
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
        from_phone = msg["from"]
        text = msg.get("text", {}).get("body", "")

        # 1) tenta buscar produtos no Shopify pelo texto
        prods = await shopify.search_product_by_title(text, limit=3)
        if prods:
            titles = [p["title"] for p in prods]
            reply = f"👋 Found {len(prods)} option(s): " + " | ".join(titles)
        else:
            # 2) fallback: IA responde
            reply = await ai.generate_reply(text, context={"from": from_phone})

        await whatsapp.send_whatsapp_text(from_phone, reply)
    except Exception as e:
        log.exception(f"Webhook error: {e}")
    return {"received": True}

# ----------------------------
# Catálogo simples do Shopify
# ----------------------------
@app.get("/catalog/products")
async def list_products(limit: int = 5):
    return await shopify.get_products(limit=limit)

# ----------------------------
# IA: endpoint de teste local
# ----------------------------
class AskBody(BaseModel):
    text: str

@app.post("/ai/ask")
async def ai_ask(body: AskBody):
    reply = await ai.generate_reply(body.text, context={"channel": "http"})
    return {"reply": reply}

# ----------------------------
# IA: listar modelos disponíveis p/ sua chave
# ----------------------------
@app.get("/ai/models")
async def ai_models():
    """
    Lista os modelos que sua API key do Gemini pode usar e os métodos suportados.
    Útil para checar o nome EXATO (às vezes vem como 'models/xxx').
    """
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.AI_API_KEY)
        models = list(genai.list_models())
        return [
            {
                "name": m.name,  # ex: 'models/gemini-1.5-pro'
                "methods": getattr(m, "supported_generation_methods", []),
            }
            for m in models
        ]
    except Exception as e:
        log.exception(f"/ai/models error: {e}")
        return {"error": str(e)}