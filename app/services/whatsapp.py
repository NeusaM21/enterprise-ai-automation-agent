import httpx
from app.config import settings
from app.utils.logger import get_logger

log = get_logger("whatsapp")
BASE = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_ID}/messages"

async def send_whatsapp_text(to: str, text: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    async with httpx.AsyncClient(timeout=20) as client:
        log.info(f"WhatsApp -> {to}: {text[:60]}")
        r = await client.post(BASE, json=payload, headers=headers)
        if r.status_code >= 400:
            log.warning(f"WA send failed {r.status_code} {r.text}")
        return r.status_code
