from app.config import settings
from app.utils.logger import get_logger

log = get_logger("ai")

async def generate_reply(user_text: str, context: dict) -> str:
    log.info(f"AI.generate_reply provider={settings.AI_PROVIDER} text={user_text[:60]}")
    return f"🤖 (MVP) You said: '{user_text}'. Soon: AI answer + Shopify catalog."
