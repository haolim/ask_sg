from pydantic_ai import Agent, ModelSettings
from ask_sg.core.intent import UserIntent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from ask_sg.core.config import settings


classifier_model_settings = ModelSettings(
    temperature=0.0
)

classifier_model = OllamaModel(
    model_name="gemma4:e4b",
    provider=OllamaProvider(settings.ollama_base_url),
    settings=classifier_model_settings
)

classifier_agent = Agent(
    model=classifier_model,
    output_type=UserIntent,
    instructions=f"""
    You are a highly precise intent classification agent for a Singapore Housing (HDB) assistant.
    Your sole task is to analyze the user's query and classify it into exactly one of the permitted intents.

    Permitted Intents:
    {UserIntent.KNOWLEDGE_BASE.value}: Use this for queries regarding historical HDB transaction data, past resale prices of past property data.
    {UserIntent.WEB_SEARCH.value}: Use this for queries about current news, latest BTO launch updates, new or upcoming housing policies, live interest rates, eligibility criteria changes, or any real-time data.

    Rules:
    Only determine the intent. Do not answer the query.
    """
)