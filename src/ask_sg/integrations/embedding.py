# Only translates (text in, vector out) so it is an adapter

from ollama import Client
from ask_sg.core.config import settings

OLLAMA_MODEL = "nomic-embed-text"
EXPECTED_DIM = 768

def embed_text(client: Client, text: str) -> list[float]:
    """Send text to Ollama and return the embedding vector."""
    response = client.embed(model=settings.ollama_embedding_model, input=text)
    embedding = response["embeddings"][0]
    assert len(embedding) == EXPECTED_DIM, (
        f"Expected {EXPECTED_DIM} dims, got {len(embedding)}"
    )
    return embedding
