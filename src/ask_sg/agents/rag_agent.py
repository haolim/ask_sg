"""
agents/rag_agent.py
The tool in this file calls the repository function to get rows, then formats them.
It doesn't contain SQL; it calls SQL.

"""

from pydantic_ai import Agent, RunContext, ModelSettings
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from ask_sg.agents.deps import AgentDeps
from ask_sg.repositories.agent_repo import get_embedding_rows
from ask_sg.core.config import settings
from ask_sg.integrations.embedding import embed_text

#qwen3 Model settings
qwen3_model_settings = ModelSettings(
    temperature=0.6,
    top_k=20,
    top_p=0.95
)

# qwen3 Model
qwen3_model = OllamaModel(
    model_name="qwen3:14b",
    provider=OllamaProvider(base_url=settings.ollama_base_url),
    settings=qwen3_model_settings
)

rag_agent = Agent(
    model=qwen3_model,
    deps_type=AgentDeps,
    instructions="""
    You answer questions about Singapore HDB resale flats. Use the retrieve_from_database tool
    to fetch relevant transactions, and base your answer ONLY on the data it returns. If
    the tool returns nothing relevant, say you don't have enough information to answer.
    
    If the question requires aggregation (averages, counts, totals) or exact filtering that
    the available tools cannot perform, say you cannot answer that type of question yet -
    do not estimate or guess.
    """
)

@rag_agent.tool
def retrieve_from_database(
    ctx: RunContext[AgentDeps],
    query: str
) -> str:
    """
    When to call this tool:
    When you need to perform semantic search against data in the Database (e.g.
    What are the recent flats sold in the town area Bishan).
    When NOT to call this tool:
    When you need to perform a specific query against data in the Database (e.g.
    Find all flats sold in Bishan or what is the average price of flats sold in Bishan).
    """
    client = ctx.deps.client
    session = ctx.deps.session
    query_vector = embed_text(client, query)
    rows = get_embedding_rows(
        session=session,
        embedding_model=settings.ollama_embedding_model,
        query_vector=query_vector,
    )
    return "\n".join(rows)
    
