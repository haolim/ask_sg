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
from typing import Any

async def get_answer(question: str,
               db: Session,
               client: Client
               ) -> str:
    deps = AgentDeps(session=db, client=client)

    async def classify_intent_node(state: State) -> dict[str, Any]:
        result = await classifier_agent.run(user_prompt=state["user_prompt"])
        return {"message_intent": result.output}
    
    async def rag_node(state: State) -> dict[str, Any]:
        result = await rag_agent.run(user_prompt=state["user_prompt"], deps=deps)
        return {"llm_response": result.output}
    
    async def web_node(state: State) -> dict[str, Any]:
        result = await web_agent.run(user_prompt=state["user_prompt"])
        return {"llm_response": result.output}
    
    graph = build_graph(
        classify_intent_node=classify_intent_node,
        rag_node=rag_node,
        web_node=web_node
    )
    result = await graph.ainvoke({"user_prompt": question})
    return result["llm_response"]


