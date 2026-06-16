# Services Layer 4
# Business logic lives here.
# Talks to the Repository.
# Never touches HTTP or raw SQL

from ollama import Client
from sqlalchemy.orm import Session
# Imports - using closure
from ask_sg.agents.graph import build_graph, State
from ask_sg.agents.classifier_agent import classifier_agent
from ask_sg.agents.rag_agent import rag_agent
from ask_sg.agents.web_agent import web_agent
from ask_sg.agents.deps import AgentDeps
from typing import Any, AsyncIterable
from langgraph.config import get_stream_writer

async def stream_answer(question: str,
               db: Session,
               client: Client
               ) -> AsyncIterable[dict[str, Any]]:
    deps = AgentDeps(session=db, client=client)

    async def classify_intent_node(state: State) -> dict[str, Any]:
        writer = get_stream_writer()
        writer({"type": "node_start", "name": "classify_intent"})
        result = await classifier_agent.run(user_prompt=state["user_prompt"])
        return {"message_intent": result.output}
    
    async def rag_node(state: State) -> dict[str, Any]:
        writer = get_stream_writer()
        writer({"type": "node_start", "name": "rag"})
        text = ""
        async with rag_agent.run_stream(user_prompt=state["user_prompt"], deps=deps) as result:
            async for delta in result.stream_text(delta=True):
                text += delta
                writer({"type": "token", "text": delta})
        return {"llm_response": text}
    
    async def web_node(state: State) -> dict[str, Any]:
        writer = get_stream_writer()
        writer({"type": "node_start", "name": "web"})
        text = ""
        async with web_agent.run_stream(user_prompt=state["user_prompt"]) as result:
            async for delta in result.stream_text(delta=True):
                text += delta
                writer({"type": "token", "text": delta})
        return {"llm_response": text}
    
    graph = build_graph(
        classify_intent_node=classify_intent_node,
        rag_node=rag_node,
        web_node=web_node
    )
    #TODO - refactor to use RunnableConfig to avoid per request inefficiency during MemorySaver dev
    async for mode, chunk in graph.astream(
        {"user_prompt": question},
        stream_mode=["updates", "custom"],
    ):
        if mode == "updates":
            for node_name in chunk:
                yield {"type": "node_end", "name": node_name}
        elif mode == "custom":
            yield chunk

