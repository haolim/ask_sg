from dataclasses import dataclass
from sqlalchemy.orm import Session # the TYPE of the session it holds
from ollama import Client # the TYPE of the embed/LLM client

@dataclass(frozen=True)
class AgentDeps:
    session: Session
    client: Client # used by the retriever tool to embed the query

