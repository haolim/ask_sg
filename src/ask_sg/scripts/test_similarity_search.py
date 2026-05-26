"""Quick test: embed a question, find similar transactions."""

import logging
from ollama import Client
from sqlalchemy import select, text
from ask_sg.core.database import SessionLocal
from ask_sg.models.orm.resale_transactions import ResaleTransactions
from ask_sg.models.orm.resale_transactions_embeddings import ResaleTransactionsEmbeddings

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

OLLAMA_MODEL = "nomic-embed-text"
TOP_K = 5

def search(question: str, top_k: int = TOP_K) -> None:
    """Embed the question and find the top-k most similar transactions."""
    client = Client()
    session = SessionLocal()

    try:
        # 1. Embed the question
        response = client.embed(model=OLLAMA_MODEL, input=question)
        query_vector = response["embeddings"][0]

        # 2. Find the top-K nearest transaction
        stmt = (
            select(
                ResaleTransactions.town,
                ResaleTransactions.flat_type,
                ResaleTransactions.floor_area_sqm,
                ResaleTransactions.resale_price,
                ResaleTransactions.sold_year,
                ResaleTransactions.flat_model,
                ResaleTransactionsEmbeddings.embedding.cosine_distance(query_vector).label("distance"),
            )
            .join(ResaleTransactionsEmbeddings,
                  ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id)
            .where(ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
            .order_by("distance")
            .limit(top_k)
        )
        results = session.execute(stmt).all()

        # 3. Print results
        print(f"\nQuestion: {question}")
        print(f"{'Town':<15} {'Type':<12} {'Sqm':<6} {'Price':<12} {'Year':<6} {'Flat Model':<18} {'Dist':<8}")
        print("-" * 90)
        for row in results:
            print(f"{row.town:<15} {row.flat_type:<12} {row.floor_area_sqm:<6} "
                  f"${row.resale_price:>10,} {row.sold_year:<6} {row.flat_model:<18} {row.distance: .4f}")
    finally:
        session.close()

if __name__ == "__main__":
    # Try a few questions
    search("affordable 4-room flat in Bishan")
    search("recent executive masionette transactions")
    search("high-floor flat near the city")