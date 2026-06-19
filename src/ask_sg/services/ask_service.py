# Services Layer 4
# Business logic lives here.
# Talks to the Repository.
# Never touches HTTP or raw SQL

from ollama import Client
from sqlalchemy.orm import Session
from ask_sg.agents.deps import AgentDeps
from typing import Any, AsyncIterable
from ask_sg.agents.graph import GRAPH_SINGLETON


async def stream_answer(question: str,
               db: Session,
               client: Client,
               thread_id: str
               ) -> AsyncIterable[dict[str, Any]]:
    deps = AgentDeps(session=db, client=client)

    async for chunk in GRAPH_SINGLETON.astream(
        {"user_prompt": question},
        config={"configurable": {"deps": deps, "thread_id": thread_id}},
        stream_mode=["updates", "custom"],
        version="v2",
    ):
        if chunk["type"] == "updates":
            for node_name in chunk["data"]:
                yield {"type": "node_end", "name": node_name}

        elif chunk["type"] == "custom":
            yield chunk["data"]

