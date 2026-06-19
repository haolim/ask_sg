# State + nodes + route_by_intent + build_graph()
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from typing import TypedDict
from ask_sg.core.intent import UserIntent
from ask_sg.agents.classifier_agent import classifier_agent
from ask_sg.agents.rag_agent import rag_agent
from ask_sg.agents.web_agent import web_agent
from langgraph.config import get_stream_writer
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain_core.runnables import RunnableConfig
from typing import Any, Annotated
import operator
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python

class State(TypedDict):
    user_prompt: str
    message_intent: UserIntent
    llm_response: str
    pydantic_messages: Annotated[list[dict], operator.add]


async def classify_intent_node(state: State) -> dict[str, Any]:
    writer = get_stream_writer()
    writer({"type": "node_start", "name": "classify_intent"})
    result = await classifier_agent.run(user_prompt=state["user_prompt"])
    return {"message_intent": result.output}

async def rag_node(state: State, config: RunnableConfig) -> dict[str, Any]:
    deps = config.get("configurable", {}).get("deps")
    if deps is None:
        raise ValueError("Critical error: Request dependencies were not injected into the graph config.")
    
    history = ModelMessagesTypeAdapter.validate_python(state.get("pydantic_messages", []))

    writer = get_stream_writer()
    writer({"type": "node_start", "name": "rag"})
    text = ""
    async with rag_agent.run_stream(user_prompt=state["user_prompt"], deps=deps, message_history=history) as result:
        async for delta in result.stream_text(delta=True):
            text += delta
            writer({"type": "token", "text": delta})
        new_msgs = to_jsonable_python(result.new_messages())
    return {"llm_response": text, "pydantic_messages": new_msgs}

async def web_node(state: State) -> dict[str, Any]:
    history = ModelMessagesTypeAdapter.validate_python(state.get("pydantic_messages", []))

    writer = get_stream_writer()
    writer({"type": "node_start", "name": "web"})
    text = ""
    async with web_agent.run_stream(user_prompt=state["user_prompt"], message_history=history) as result:
        async for delta in result.stream_text(delta=True):
            text += delta
            writer({"type": "token", "text": delta})
        new_msgs = to_jsonable_python(result.new_messages()) # scoped to func.
    return {"llm_response": text, "pydantic_messages": new_msgs}

def build_graph(
        classify_intent_node,
        rag_node,
        web_node,
        checkpointer: BaseCheckpointSaver
        ) -> CompiledStateGraph:
    
    def route_decision(state: State) -> UserIntent:
        return state["message_intent"]

    graph_builder = StateGraph(State)

    graph_builder.add_node("classify_intent", classify_intent_node)
    graph_builder.add_node("rag", rag_node)
    graph_builder.add_node("web", web_node)

    graph_builder.add_edge(
        START, "classify_intent"
    )

    graph_builder.add_conditional_edges(
        "classify_intent",
            route_decision,
            {UserIntent.KNOWLEDGE_BASE: "rag",
                UserIntent.WEB_SEARCH: "web"}
    )

    graph_builder.add_edge(
        "rag", END
    )
    graph_builder.add_edge(
        "web", END
    )

    return graph_builder.compile(checkpointer=checkpointer)

GRAPH_SINGLETON = build_graph(
    classify_intent_node=classify_intent_node,
    rag_node=rag_node,
    web_node=web_node,
    checkpointer=MemorySaver()
)
