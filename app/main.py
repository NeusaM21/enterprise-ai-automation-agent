# app/main.py
from __future__ import annotations

import os
import time
import asyncio
from typing import Optional, List

from fastapi import FastAPI, Request, Query, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()  # garante que o .env esteja carregado o quanto antes

from app.config import settings
from app.utils.logger import get_logger
from app.services import ai, shopify, whatsapp

log = get_logger("app")
app = FastAPI(
    title="Enterprise AI Automation Agent",
    version="0.2.0",
    description="Backend FastAPI para automações com IA, integrações e webhooks."
)

# ----------------------------
# Root (info rápida)
# ----------------------------
@app.get("/")
async def root():
    return {
        "name": "Enterprise AI Automation Agent",
        "env": settings.ENV,
        "docs": "/docs",
        "health": "/health",
        "ai": {"ask": "/ai/ask", "models": "/ai/models"},
        "webhooks": {"whatsapp": "/webhook/whatsapp"},
    }

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
    log.info(f"WA webhook: {str(body)[:500]}")  # evita flood no log
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
        from_phone = msg["from"]
        text = msg.get("text", {}).get("body", "") or ""

        # 1) tenta buscar produtos no Shopify pelo texto
        prods = await shopify.search_product_by_title(text, limit=3)
        if prods:
            titles = [p.get("title", "Untitled") for p in prods]
            reply = f"👋 Found {len(prods)} option(s): " + " | ".join(titles)
        else:
            # 2) fallback: IA responde
            reply = await ai.generate_reply(text, context={"from": from_phone, "channel": "whatsapp"})

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
# IA: modelos disponíveis p/ sua chave
# ----------------------------
@app.get("/ai/models")
async def ai_models():
    """
    Lista os modelos que sua API key do Gemini pode usar e os métodos suportados.
    Útil para checar o nome EXATO (ex: 'models/gemini-2.5-flash').
    """
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.AI_API_KEY)
        models = list(genai.list_models())
        payload = [
            {
                "name": m.name,  # ex: 'models/gemini-2.5-flash'
                "methods": getattr(m, "supported_generation_methods", []),
            }
            for m in models
        ]
        # ordena por nome pra ficar determinístico
        payload.sort(key=lambda x: x.get("name", ""))
        return payload
    except Exception as e:
        log.exception(f"/ai/models error: {e}")
        return {"error": str(e)}

# ----------------------------
# IA: endpoint reforçado /ai/ask
# ----------------------------
class AskBody(BaseModel):
    text: str
    model: Optional[str] = None        # permite override por requisição
    timeout_ms: Optional[int] = None   # permite override do timeout (default 30s)

DEFAULT_MODEL_CANDIDATES: List[str] = [
    # ordem de preferência
    getattr(settings, "AI_MODEL", None) or "",
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro",
    "models/gemini-2.0-flash-001",
]

async def _choose_model(preferred: Optional[str]) -> tuple[str, bool]:
    """
    Retorna (model_escolhido, usou_fallback?)
    """
    # 1) pega modelos disponíveis
    try:
        available = [m["name"] for m in await ai_models()]  # reaproveita o endpoint local
    except Exception:
        # fallback: se /ai/models falhar, tenta seguir com o preferido
        available = []

    # 2) constrói lista de preferências
    prefs = []
    if preferred:
        prefs.append(preferred)
    prefs.extend([m for m in DEFAULT_MODEL_CANDIDATES if m])

    # 3) decide
    for cand in prefs:
        if not available or cand in available:
            return cand, (cand != preferred)
    # 4) último caso: se houver lista disponível, usa a primeira
    if available:
        return available[0], True
    # 5) sem nada disponível: volta no preferred (mesmo sem validar)
    return preferred or "models/gemini-2.5-flash", True

@app.post("/ai/ask")
async def ai_ask(body: AskBody):
    """
    Faz uma pergunta ao provedor configurado.

    Retorno padrão:
    {
      "model": "models/gemini-2.5-flash",
      "fallback": false,
      "latency_ms": 123,
      "reply": "texto"
    }
    """
    # define timeout (default 30s)
    timeout_s: float = max(1, (body.timeout_ms or 30000) / 1000.0)

    # escolhe modelo (valida e aplica fallback se necessário)
    preferred_model = body.model or getattr(settings, "AI_MODEL", None)
    model, used_fallback = await _choose_model(preferred_model)

    # chama a IA com timeout e mede latência
    t0 = time.perf_counter()
    try:
        # ai.generate_reply deve ser async e aceitar contexto (mantendo compat)
        reply: str = await asyncio.wait_for(
            ai.generate_reply(body.text, context={"channel": "http", "model": model}),
            timeout=timeout_s
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail=f"AI request timed out after {int(timeout_s*1000)} ms")
    except Exception as e:
        log.exception(f"/ai/ask provider error: {e}")
        raise HTTPException(status_code=502, detail=f"AI provider error: {e}")

    latency_ms = int((time.perf_counter() - t0) * 1000)

    # log “limpo” (evita logar prompts/respostas gigantes)
    log.info(f"/ai/ask ok model={model} fallback={used_fallback} latency_ms={latency_ms} text_len={len(body.text)} reply_len={len(reply)}")

    return {
        "model": model,
        "fallback": bool(used_fallback),
        "latency_ms": latency_ms,
        "reply": reply,
    }