from fastapi import FastAPI, Request, Query, HTTPException
from app.config import settings
from app.utils.logger import get_logger
from app.services import ai, shopify, whatsapp

log = get_logger("app")
app = FastAPI(title="Enterprise AI Automation Agent")

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENV}

@app.get("/webhook/whatsapp")
async def verify(mode: str | None = Query(None),
                 challenge: str | None = Query(None),
                 token: str | None = Query(None)):
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(challenge) if challenge and challenge.isdigit() else (challenge or "OK")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook/whatsapp")
async def receive(req: Request):
    body = await req.json()
    log.info(f"WA webhook: {str(body)[:500]}")
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
        from_phone = msg["from"]
        text = msg.get("text", {}).get("body", "")

        prods = await shopify.search_product_by_title(text, limit=3)
        if prods:
            titles = [p["title"] for p in prods]
            reply = f"👋 Found {len(prods)} option(s): " + " | ".join(titles)
        else:
            reply = await ai.generate_reply(text, context={"from": from_phone})

        await whatsapp.send_whatsapp_text(from_phone, reply)
    except Exception as e:
        log.exception(f"Webhook error: {e}")
    return {"received": True}

@app.get("/catalog/products")
async def list_products(limit: int = 5):
    return await shopify.get_products(limit=limit)
