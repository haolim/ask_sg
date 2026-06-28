from dataclasses import dataclass, field
from sqlalchemy.orm import Session # the TYPE of the session it holds
from ollama import Client # the TYPE of the embed/LLM client

@dataclass(frozen=False)
class AgentDeps:
    session: Session
    client: Client # used by the retriever tool to embed the query
    retrieved: list[str] = field(default_factory=list)