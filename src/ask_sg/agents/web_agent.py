
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from ask_sg.core.config import settings
from tavily import AsyncTavilyClient


async def tavily_search(query: str) -> str:
    """Search the web for up-to-date real-time information specifically 
    about Singapore HDB flats, news, policies, and grants.
    
    Args:
        query: The raw search query string to look up.
    """
    target_domains = [
        "www.hdb.gov.sg", 
        "www.channelnewsasia.com", 
        "www.straitstimes.com"
    ]
    tavily_client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    response = await tavily_client.search(
        query=query, 
        max_results=3,
        include_domains=target_domains
        )
    return str(response)

web_llm_model_settings = ModelSettings(
    temperature=0.6,
    top_k=20,
    top_p=0.95
)

web_llm_model = OllamaModel(
    model_name="qwen3.5:9b",
    provider=OllamaProvider(settings.ollama_base_url),
    settings=web_llm_model_settings
)

web_agent = Agent(
    model=web_llm_model,
    tools=[tavily_search],
    instructions=
    """
    You are a specialized Web Search Agent tasked with answering questions about 
    Singapore HDB resale flats using real-time information. 

    CRITICAL ACTIONS:
    1. Trigger the web search tool for every query to ensure the most up-to-date data.
    2. Prioritize official sources (e.g., HDB InfoWEB, Ministry of National Development) 
    or reputable local news (e.g., Straits Times, CNA) found in the search results.
    3. Base your answer ONLY on the explicit facts returned by the tool. Do not use 
    pre-trained knowledge about HDB prices, grants, or policies.

    GUARDRAILS & LIMITATIONS:
    - If the search results contain conflicting data, state the conflict and cite the sources. 
    - If the search results do not contain the specific answer, or if the sources look 
    unreliable/outdated, state clearly that you do not have enough verified, 
    up-to-date information to answer.
    - If the question requires data aggregation (averages, calculations, totals) or 
    complex multi-criteria filtering that the raw search snippets cannot precisely 
    provide, state: "I cannot calculate or aggregate that data precisely based on 
    current search results." Do not estimate or guess.

    TONE: 
    Objective, factual, and direct. Always cite or mention the source of the 
    information you are quoting (e.g., "According to the latest HDB press release...").
    """
)

