from ask_sg.agents.graph import build_graph
from ask_sg.agents.classifier_agent import classifier_agent
from ask_sg.agents.rag_agent import rag_agent
from ask_sg.agents.web_agent import web_agent
from ask_sg.core.database import SessionLocal
from ask_sg.integrations.ollama_client import ollama_embedding_client
from ask_sg.core.intent import UserIntent
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TEST_QUERY = [
    # --- Historical Queries (RAG) ---
    {
        "query": "What were average HDB prices in Bishan last quarter?",
        "expected_intent": UserIntent.KNOWLEDGE_BASE,
    },
    {
        "query": "What are the resale prices of the 5-room flat at Punggol?",
        "expected_intent": UserIntent.KNOWLEDGE_BASE
    },
    {
        "query": "Show me the resale history, including previous transaction prices, for flats in Ang Mo Kio.",
        "expected_intent": UserIntent.KNOWLEDGE_BASE
    },
    {
        "query": "What was the remaining lease of the 3-room flat sold at Tampines Street 21 last month?",
        "expected_intent": UserIntent.KNOWLEDGE_BASE
    },
    {
        "query": "Find the transaction price for a 4-room flat in Bishan sold in January 2024.",
        "expected_intent": UserIntent.KNOWLEDGE_BASE
    },
    # --- Current / News Queries (WEB) ---
    {
        "query": "What are the latest BTO grants for first-time buyers?",
        "expected_intent": UserIntent.WEB_SEARCH
    },
    {
        "query": "What are the latest HDB loan interest rates and CPF housing grant limits announced for this year?",
        "expected_intent": UserIntent.WEB_SEARCH
    },
    {
        "query": "Can a single person buy a resale Plus or Prime flat under the newest HDB framework?",
        "expected_intent": UserIntent.WEB_SEARCH
    },
    {
        "query": "What are the clawback subsidy percentage rules when selling a Prime location resale flat?",
        "expected_intent": UserIntent.WEB_SEARCH
    },
    {
        "query": "Are there any recent policy updates regarding the resale eligibility of 3-generation (3Gen) flats?",
        "expected_intent": UserIntent.WEB_SEARCH
    }
]

async def main():
    graph = build_graph(
    classifier_agent=classifier_agent,
    rag_agent=rag_agent,
    web_search_agent=web_agent,
    session_factory=SessionLocal,
    ollama_client=ollama_embedding_client
    )

    logger.info("Running classification tests...")

    passed_count = 0
    failed_cases = []
    passed_cases = []
    total_tests = len(TEST_QUERY)

    for i, case in enumerate(TEST_QUERY, start=1):
        query = case["query"]
        expected = case["expected_intent"]

        try:
            result = await graph.ainvoke({"user_prompt": query})
            actual_intent = result.get("message_intent")

            if actual_intent == expected:
                passed_cases.append(case)
                passed_count += 1
            else:
                failed_cases.append(case)
        except Exception as e:
            logger.info(f"Test {i} crashed with error: {e}\n")

    if passed_cases:
        passed_summary = '\n\n'.join(
            '\n'.join(f" {k}: {v}" for k, v in case.items())
            for case in passed_cases
        )
    else:
        passed_summary = " None!"

    if failed_cases:
        failed_summary = '\n\n'.join(
            '\n'.join(f" {k}: {v}" for k, v in case.items())
            for case in failed_cases
        )
    else:
        failed_summary = " None!"

    logger.info("=" * 90)
    logger.info(f"""
          SUMMARY: 
          {passed_count}/{total_tests} test cases passed.

          The following test cases passed:
          {passed_summary}

          The following test cases failed:
          {failed_summary}
          
          """)
    logger.info("=" * 90)

if __name__ == "__main__":
    asyncio.run(main())

# try:
#     # Generate the PNG binary data using the Mermaid API
#     png_data = graph.get_graph().draw_mermaid_png()

#     # Write the binary data to a file
#     with open("langgraph_graph_output.png", "wb") as f:
#         f.write(png_data)
#     print("Successfully saved graph as langgraph_graph_output.png")

# except Exception as e:
#     print(f"Could not generate PNG: {e}")
