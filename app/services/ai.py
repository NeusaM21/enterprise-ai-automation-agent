# app/services/ai.py

import asyncio
import logging
# Importa as exceções específicas do Google para tratamento de erros no try/except
from google.api_core.exceptions import PermissionDenied, NotFound, InvalidArgument, ResourceExhausted
# Importa 'settings' para acessar AI_MODEL e SYSTEM_PROMPT
from app.config import settings 
# Importa a função síncrona de geração, que será executada em um thread
from app.services.gemini_client import _sync_generate 

# Configuração do logger para registrar erros
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def _gen_gemini(user_text: str, context: dict) -> str:
    """
    Função auxiliar que monta o prompt e executa a chamada síncrona ao Gemini 
    em um thread separado (asyncio.to_thread) para evitar bloqueio do loop de eventos do FastAPI.
    """
    try:
        # 1. Obtém o nome do modelo (do contexto se sobrescrito, senão do settings)
        model_name: str = context.get("model", settings.AI_MODEL) 

        # 2. Montando o prompt usando settings.SYSTEM_PROMPT
        prompt = f"{settings.SYSTEM_PROMPT}\n\nUser message: {user_text}\n\nContext: {context}"

        # 3. EXECUTA a função síncrona (_sync_generate) em um thread pool
        #    Passa o nome do modelo e o prompt.
        reply = await asyncio.to_thread(_sync_generate, model_name, prompt)

        return reply  # Retorna a resposta gerada pelo modelo

    except PermissionDenied as e:
        # Erro comum: Chave de API inválida
        logger.error(f"Permission denied (Invalid API Key): {e}", exc_info=True)
        return "Sorry, I don't have permission to access the AI model. Please check your API key."

    except NotFound as e:
        # Erro comum: Nome do modelo incorreto
        logger.error(f"Model not found: {e}", exc_info=True)
        return "The requested AI model is not available. Please verify the model name."
        
    except InvalidArgument as e:
        # Erro comum: Prompt malformado ou conteúdo bloqueado (safety settings)
        logger.error(f"AI argument or content error: {e}", exc_info=True)
        return "There was an issue with the AI request (e.g., malformed prompt or content filtering)."
    
    except ResourceExhausted as e:
        # Erro de Rate Limit
        logger.error(f"AI rate limit exceeded: {e}", exc_info=True)
        return "The AI service is busy right now. Please try again later."

    except Exception as e:
        # Captura qualquer outro erro inesperado (rede, timeout, etc.)
        logger.error(f"An unexpected error occurred during AI call: {e}", exc_info=True)
        return "Sorry, I had trouble accessing the AI right now."


async def generate_reply(user_text: str, context: dict) -> str:
    """
    Função pública (usada pelo main.py/webhook) que gera uma resposta da IA.
    """
    try:
        # Chama a função auxiliar que contém a lógica de execução em thread
        reply = await _gen_gemini(user_text, context)
        return reply

    except Exception as e:
        # Trata erros inesperados do wrapper (improvável, mas seguro)
        logger.error(f"Error in public generate_reply wrapper: {e}", exc_info=True)
        return "Sorry, I was unable to generate a response. Please try again later."