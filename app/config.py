# app/config.py
# --------------------------------------------
# ✅ Configuration module for the Enterprise AI Automation Agent
# Loads environment variables safely and provides global settings access.
# --------------------------------------------

from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load variables from .env file (works in both local and production)
load_dotenv()

class Settings(BaseModel):
    # 🧩 Environment & Server
    ENV: str = os.getenv("ENV", "dev")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # 🤖 AI Configuration (Gemini / OpenAI)
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "google")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "models/gemini-2.5-flash")

    # 🛍️ Shopify Configuration
    SHOPIFY_STORE_DOMAIN: str = os.getenv("SHOPIFY_STORE_DOMAIN", "")
    SHOPIFY_ADMIN_API_KEY: str = os.getenv("SHOPIFY_ADMIN_API_KEY", "")
    SHOPIFY_ADMIN_API_VERSION: str = os.getenv("SHOPIFY_ADMIN_API_VERSION", "2024-07")

    # 💬 WhatsApp Configuration
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID: str = os.getenv("WHATSAPP_PHONE_ID", "")

    # ⚙️ Redis / Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # 🔒 Validation / Debug Helper
    def validate_env(self):
        """Check if critical variables are loaded; print warnings if missing."""
        if not self.AI_API_KEY:
            print("⚠️ Warning: Missing AI_API_KEY. Gemini responses may fallback.")
        if not self.AI_MODEL:
            print("⚠️ Warning: Missing AI_MODEL. Defaulting to gemini-2.5-flash.")
        if not self.WHATSAPP_TOKEN:
            print("⚠️ Warning: WhatsApp integration not configured.")
        if not self.SHOPIFY_ADMIN_API_KEY:
            print("⚠️ Warning: Shopify API key missing.")
        print("✅ Environment variables successfully loaded from .env.")

# Instantiate global settings
settings = Settings()

# Optional validation log when app starts
settings.validate_env()