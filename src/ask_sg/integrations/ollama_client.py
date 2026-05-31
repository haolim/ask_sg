from ollama import Client
from ask_sg.core.config import settings

ollama_embedding_client = Client(
    host=settings.ollama_embedding_model_base_url
)