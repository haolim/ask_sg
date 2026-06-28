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

#RAG Model settings
#TODO(config): extract ModelSettings to be injectable config (allow different production temp and eval temp)
rag_model_settings = ModelSettings(
    temperature=0.0,
    top_k=20,
    top_p=0.95
)

# RAG Model
rag_model = OllamaModel(
    model_name="qwen3.5:9b",
    provider=OllamaProvider(base_url=settings.ollama_base_url),
    settings=rag_model_settings
)

rag_agent = Agent(
    model=rag_model,
    deps_type=AgentDeps,
    instructions="""
    You answer questions about Singapore HDB resale flats.

    Step 1: Check if the question requires aggregation (average, count, total, range,
    or other computed statistics) or exact filtering the tools cannot perform.
    If so, respond with EXACTLY this sentence and nothing else:
    "I cannot answer that type of question yet."
    Do not call retrieve_from_database for this type of question. Stop here.

    Step 2: Otherwise, use the retrieve_from_database tool to fetch relevant transactions.
    Base your answer ONLY on the data returned. Do not add observations, summaries,
    or reformat the listing beyond presenting it clearly.

    Step 3: If the tool returns nothing relevant to the question, say you don't have
    enough information to answer. Do not estimate, guess, or describe unrelated
    transactions that were retrieved.
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
    # .extend as agent may loop and we want to append elements to existing list
    # as an iterable so that it is flattened and not a list of lists
    ctx.deps.retrieved.extend(rows)
    return "\n".join(rows)
    
