# State + nodes + route_by_intent + build_graph()
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Any
from enum import Enum

class UserIntent(Enum):
    KNOWLEDGE_BASE = "search_vector_database"
    WEB_SEARCH = "search_public_internet"

class State(TypedDict):
    user_prompt: str
    message_intent: UserIntent
    retrieved_context: str
    llm_response: str


def classify_intent_node(state: State) -> dict[str, Any]:
    print("---CLASSIFY INTENT STEP---")
    chosen_intent: UserIntent = UserIntent.KNOWLEDGE_BASE
    print(chosen_intent.value)
    return {"message_intent": chosen_intent}


def rag_retrieval_node(state: State) -> dict[str, Any]:
    return {"retrieved_context": "Context from Vector DB"}


def web_search_node(state: State) -> dict[str, Any]:
    return {"retrieved_context": "Context from Search"}


def generate_response_node(state: State) -> dict[str, Any]:
    return {"llm_response": "Resposne from LLM"}

def route_decision(state: State) -> Literal["rag_retrieval", "web_search"]:
    print("---ROUTING DECISION---")
    if state["message_intent"] == UserIntent.KNOWLEDGE_BASE:
        print("rag_retrieval")
        return "rag_retrieval"
    print("web search")
    return "web_search"


graph_builder = StateGraph(State)

graph_builder.add_node(
    "classify_intent", classify_intent_node
)
graph_builder.add_node(
    "rag_retrieval", rag_retrieval_node
)
graph_builder.add_node(
    "web_search", web_search_node
)
graph_builder.add_node(
    "generate_response", generate_response_node
)
graph_builder.add_edge(
    START, "classify_intent"
)
graph_builder.add_conditional_edges(
    "classify_intent",
        route_decision
)
graph_builder.add_edge(
    "rag_retrieval", "generate_response"
)
graph_builder.add_edge(
   "web_search", "generate_response"
)
graph_builder.add_edge(
    "generate_response", END
)

graph = graph_builder.compile()

result = graph.invoke(
    {"user_prompt": "Show me some recent HDB resale transactions for the town 'Tampines'"}
)
print(*(f"{k}: {v}" for k, v in result.items()))

try:
    # Generate the PNG binary data using the Mermaid API
    png_data = graph.get_graph().draw_mermaid_png()

    # Write the binary data to a file
    with open("langgraph_graph_output.png", "wb") as f:
        f.write(png_data)
    print("Successfully saved graph as langgraph_graph_output.png")

except Exception as e:
    print(f"Could not generate PNG: {e}")

