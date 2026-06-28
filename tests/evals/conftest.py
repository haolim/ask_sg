import pytest
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ollama import Client
from ask_sg.core.database import SessionLocal
from ask_sg.core.config import settings

@pytest.fixture(scope="session")
def evaluator_llm():
    client = AsyncOpenAI(
        api_key="ollama",
        base_url=settings.ollama_base_url
    )
    """
    Tested mistral-nemo:12b - unreliable (it ranked first 5 as relevant and next 5 as irrelevant when all 10 retrieved chunks were relevant)
    Tested gemma4:12b, qwen3.5:9b - took too long and ran out of tokens due to 'thinking'
    """
    llm = llm_factory(
        "qwen2.5:14b", 
        provider="openai", 
        client=client,
        max_tokens=8192
        )
    print("IS_ASYNC:", getattr(llm, "is_async", "no such attr"))
    return llm


@pytest.fixture(scope="session")
def client():
    return Client(host=settings.ollama_embedding_model_base_url)


@pytest.fixture(scope="function")
def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

