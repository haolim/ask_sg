# State + nodes + route_by_intent + build_graph()
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from typing import TypedDict
from ask_sg.core.intent import UserIntent

class State(TypedDict):
    user_prompt: str
    message_intent: UserIntent
    llm_response: str


def build_graph(
        classify_intent_node,
        rag_node,
        web_node,
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
    
    return graph_builder.compile()

