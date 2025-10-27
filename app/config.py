# app/config.py

import os
import logging
from typing import Optional

from pydantic import BaseModel
from dotenv import load_dotenv

# Forçar carregamento do .env
# Este caminho deve ser ajustado se o .env não estiver na raiz.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")) 

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("config")

class Settings(BaseModel):
    """
    Módulo de configuração que carrega variáveis de ambiente e
    fornece acesso global às configurações.
    """
    
    # ----------------------------
    # Environment & Server
    # ----------------------------
    ENV: str = os.getenv("ENV", "dev")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ----------------------------
    # AI Configuration (Gemini / OpenAI)
    # ----------------------------
    # Variável GLOBAL para o prompt do sistema (usada no ai.py)
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are an Enterprise AI Automation Agent. Be concise, polite, and helpful, focused on e-commerce support."
    )

    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "google")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    # Remove 'models/' prefix if present in AI_MODEL
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash").replace("models/", "").strip() 
    
    # ----------------------------
    # Shopify Configuration
    # ----------------------------
    SHOPIFY_STORE_DOMAIN: str = os.getenv("SHOPIFY_STORE_DOMAIN", "shop-name.myshopify.com")
    SHOPIFY_ADMIN_API_KEY: str = os.getenv("SHOPIFY_ADMIN_API_KEY", "")
    SHOPIFY_ADMIN_API_VERSION: str = os.getenv("SHOPIFY_ADMIN_API_VERSION", "2024-07")

    # ----------------------------
    # WhatsApp Configuration
    # ----------------------------
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID: str = os.getenv("WHATSAPP_PHONE_ID", "")
    
    # ----------------------------
    # Redis / Cache
    # ----------------------------
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Instancia as configurações globais
settings = Settings()


def validate_env():
    """
    Verificação de variáveis críticas no ambiente.
    A função original foi movida para fora da classe, mas ainda usa 'settings'.
    """
    logger.info(f"🔍 AI_MODEL from .env: {settings.AI_MODEL}")
    
    if not settings.AI_API_KEY:
        logger.warning("🚨 WARNING: Missing AI_API_KEY. Gemini responses may fallback or fail.")
        
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_VERIFY_TOKEN:
        logger.warning("🚨 WARNING: WhatsApp Integration not fully configured.")
        
    if not settings.SHOPIFY_ADMIN_API_KEY:
        logger.warning("🚨 WARNING: Shopify API key missing.")
        
    logger.info("✅ Environment variables successfully loaded from .env.")


# Validação opcional para quando o app inicia
validate_env()