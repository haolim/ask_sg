# State + nodes + route_by_intent + build_graph()
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from typing import TypedDict, Any, Callable
from pydantic_ai import Agent
from sqlalchemy.orm import Session
from ollama import Client
from ask_sg.agents.deps import AgentDeps
from ask_sg.core.intent import UserIntent

class State(TypedDict):
    user_prompt: str
    message_intent: UserIntent
    llm_response: str


def build_graph(
        classifier_agent: Agent[None, UserIntent],
        rag_agent: Agent[AgentDeps, None],
        web_search_agent: Agent[None, None],
        session_factory: Callable[[], Session],
        ollama_client: Client,
        ) -> CompiledStateGraph:
    
    async def classify_intent_node(state: State) -> dict[str, Any]:
        result = await classifier_agent.run(user_prompt=state["user_prompt"])
        return {"message_intent": result.output}
    
    async def rag_agent_node(state: State) -> dict[str, Any]:
        with session_factory() as sess:
            current_deps = AgentDeps(
                session=sess,
                client=ollama_client
            )

            result = await rag_agent.run(
                user_prompt=state["user_prompt"],
                deps=current_deps
            )      
            return {"llm_response": result.output}
        
    async def web_search_agent_node(state: State) -> dict[str, Any]:
        result = await web_search_agent.run(user_prompt=state["user_prompt"])
        return {"llm_response": result.output}

    def route_decision(state: State) -> UserIntent:
        return state["message_intent"]

    graph_builder = StateGraph(State)

    graph_builder.add_node(
        "classify_intent", classify_intent_node
    )
    graph_builder.add_node(
        "rag_agent", rag_agent_node
    )
    graph_builder.add_node(
        "web_agent", web_search_agent_node
    )
    graph_builder.add_edge(
        START, "classify_intent"
    )
    graph_builder.add_conditional_edges(
        "classify_intent",
            route_decision,
            {UserIntent.KNOWLEDGE_BASE: "rag_agent",
             UserIntent.WEB_SEARCH: "web_agent"}
    )
    graph_builder.add_edge(
        "rag_agent", END
    )
    graph_builder.add_edge(
    "web_agent", END
    )

    
    return graph_builder.compile()

