import google.generativeai as genai
from google.api_core.exceptions import PermissionDenied, NotFound, InvalidArgument
from app.config import settings

# A função _configure_gemini foi embutida no _sync_generate para garantir a 
# configuração em cada thread pool, o que é mais seguro.

def _sync_generate(model_name: str, prompt: str) -> str:
    """
    Função síncrona para gerar conteúdo usando o modelo do Gemini.
    O 'ai.py' deve rodar esta função em um 'asyncio.to_thread'.
    """
    
    # 1. Configura a chave de API
    if not settings.AI_API_KEY:
        raise PermissionError("Missing AI_API_KEY in settings.")
    
    # Configuração da chave de API (necessária em cada thread)
    genai.configure(api_key=settings.AI_API_KEY)
    
    try:
        # 2. Instancia e usa o modelo
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt)
        
        # O .generate_content pode retornar um Candidate com .text vazio se for bloqueado
        if not response.text:
            raise InvalidArgument("The model response was empty, possibly due to safety settings or a malformed prompt.")
            
        return response.text
        
    except (NotFound, InvalidArgument, PermissionDenied) as e:
        # Relança as exceções específicas para que o ai.py possa tratá-las
        raise e
        
    except Exception as e:
        # Captura outros erros desconhecidos do SDK ou de rede
        raise RuntimeError(f"Unknown error during Gemini generation: {e}")