from ask_sg.integrations.ollama_client import ollama_embedding_client
from ollama import Client

def get_ollama_client() -> Client:
    return ollama_embedding_client