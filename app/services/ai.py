# app/services/ai.py
import asyncio
from app.config import settings
from app.utils.logger import get_logger

log = get_logger("ai")

# --- Gemini SDK ---
try:
    import google.generativeai as genai
    _HAS_GENAI = True
except Exception as e:
    log.warning(f"Gemini SDK not available: {e}")
    _HAS_GENAI = False

# --- Persona / System prompt ---
SYSTEM_PROMPT = (
    "You are an AI Sales & Support Agent for an e-commerce store. "
    "Be concise, proactive and friendly. If the user asks about products, "
    "use any provided context (e.g., Shopify titles/attributes). "
    "If information is missing, ask a short clarifying question. "
    "Prefer short paragraphs and bullet points. Keep answers under 120 words."
)

def _ensure_client():
    """
    Configure the Gemini client once per request.
    Raises if SDK/key are missing.
    """
    if not _HAS_GENAI:
        raise RuntimeError("google-generativeai SDK is not installed.")
    if not settings.AI_API_KEY:
        raise RuntimeError("AI_API_KEY is empty. Set your Gemini API key in .env")
    genai.configure(api_key=settings.AI_API_KEY)
    return genai.GenerativeModel(settings.AI_MODEL or "gemini-1.5-flash")

def _sync_generate(model, prompt: str) -> str:
    """
    SDK é síncrono; rodamos em thread pra não travar o loop async.
    """
    resp = model.generate_content([{"role": "user", "parts": [prompt]}])
    text = getattr(resp, "text", "") or ""
    return text.strip() or "I couldn't generate a response right now."

async def _gen_gemini(user_text: str, context: dict) -> str:
    model = _ensure_client()
    prompt = f"{SYSTEM_PROMPT}\n\nUser message: {user_text}\n\nContext: {context}"
    return await asyncio.to_thread(_sync_generate, model, prompt)

# ---- Public API used by the FastAPI app ----
async def generate_reply(user_text: str, context: dict) -> str:
    provider = (settings.AI_PROVIDER or "gemini").lower()
    log.info(f"AI.generate_reply provider={provider} model={settings.AI_MODEL} text={user_text[:60]}")
    if provider == "gemini":
        try:
            return await _gen_gemini(user_text, context)
        except Exception as e:
            log.exception(f"Gemini error: {e}")
            return "Sorry, I had trouble accessing the AI right now."
    # fallback (se algum dia trocarmos provider e não implementar ainda)
    return f"(stub) You said: '{user_text}'"
