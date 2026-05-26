"""Generate embeddings for resale transactions and store in pgvector column"""
import logging
from typing import Iterable, Sequence
from ollama import Client
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from tqdm import tqdm
from ask_sg.core.database import SessionLocal
from ask_sg.models.orm.resale_transactions import ResaleTransactions
from ask_sg.models.orm.resale_transactions_embeddings import ResaleTransactionsEmbeddings
from uuid import UUID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
# SILENCE THE HTTP SPAM:
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

OLLAMA_MODEL = "nomic-embed-text"
EXPECTED_DIM = 768
COMMIT_EVERY = 500


def embed_text(client: Client, text: str) -> list[float]:
    """Send text to Ollama and return the embedding vector."""
    response = client.embed(model=OLLAMA_MODEL, input=text)
    embedding = response["embeddings"][0]
    assert len(embedding) == EXPECTED_DIM, (
        f"Expected {EXPECTED_DIM} dims, got {len(embedding)}"
    )
    return embedding

def get_unembedded_ids(session: Session) -> list[UUID]:
    """Get IDs of transactions that don't yet have an embedding for our target model."""
    stmt = (
        select(ResaleTransactions.id)
        .outerjoin(
            ResaleTransactionsEmbeddings,
            (ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id) &
            (ResaleTransactionsEmbeddings.transaction_id.is_(None))
        )
        .filter(ResaleTransactions.embedding_text.isnot(None))
        .filter(ResaleTransactionsEmbeddings.transaction_id.is_(None))
    )
    return list(session.scalars(stmt).all())

# def iter_unembedded(session: Session, batch_size: int) -> Iterable[Sequence[ResaleTransactions]]:
#     """Stream transactions that don't yet have an embedding for our target model.
    
#     Returns a Partitioned Results iterable using SQLAlchemy 2.0 style syntax.
#     """
#     # subquery = (
#     #     select(ResaleTransactionsEmbeddings.transaction_id)
#     #     .filter(ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#     #     # session.query(
#     #     #     ResaleTransactionsEmbeddings.transaction_id
#     #     # )
#     #     # .filter(ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#     # )
#     stmt = (
#         select(ResaleTransactions)
#         .outerjoin(
#             ResaleTransactionsEmbeddings,
#             (ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id) &
#             (ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#         )
#         .filter(ResaleTransactions.embedding_text.isnot(None))
#         #.filter(ResaleTransactions.id.notin_(subquery))
#         # Checks where the joined embedding table has no match
#         .filter(ResaleTransactionsEmbeddings.transaction_id.is_(None))
#         .execution_options(yield_per=batch_size)
#         #.limit(500)
#     )
#     return session.scalars(stmt).partitions()
#     # return (
#     #     session.query(ResaleTransactions)
#     #     .filter(ResaleTransactions.embedding_text.isnot(None))
#     #     .filter(ResaleTransactions.id.notin_(subquery))
#     #     .yield_per(batch_size)
#     #     )

# def count_unembedded(session: Session) -> int:
#     """Count transactions that don't yet have an embedding for our target model."""
#     # subquery = (
#     #     session.query(ResaleTransactionsEmbeddings.transaction_id)
#     #     .filter(ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#     # )
#     # return (
#     #     session.query(ResaleTransactions)
#     #     .filter(ResaleTransactions.embedding_text.isnot(None))
#     #     .filter(ResaleTransactions.id.notin_(subquery))
#     #     .count()
#     # )
#     # subquery = (
#     #     select(ResaleTransactionsEmbeddings.transaction_id)
#     #     .filter(ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#     # )
#     stmt = (
#         select(func.count(ResaleTransactions.id))
#         .outerjoin(
#             ResaleTransactionsEmbeddings,
#             (ResaleTransactions.id == ResaleTransactionsEmbeddings.transaction_id) &
#             (ResaleTransactionsEmbeddings.embedding_model == OLLAMA_MODEL)
#         )
#         .filter(ResaleTransactions.embedding_text.isnot(None))
#         .filter(ResaleTransactionsEmbeddings.transaction_id.is_(None))
#         #.filter(ResaleTransactions.id.notin_(subquery))
#     )
#     return session.scalar(stmt)
#     # Modern 2.0 connection style execution for count scalar operations
#     #return len(session.scalars(stmt).all())

def main() -> None:
    client = Client()
    session = SessionLocal()

    ids_to_process = get_unembedded_ids(session)
    total_remaining = len(ids_to_process)
    logger.info(f"Found {total_remaining:,} rows to embed")

    success_count = 0
    failure_count = 0

    try:
        logger.info(f"Starting embedding generation with "
        f"model={OLLAMA_MODEL} " 
        f"batch_size={COMMIT_EVERY}"
        )
        with tqdm(total=total_remaining, desc="Generating Embeddings", unit="rows") as pbar:
            # 2. Iterate cleanly through chunks of data provided by the DB driver
            for idx, row_id in enumerate(ids_to_process, start=1):
                try:
                    row = session.get(ResaleTransactions, row_id)
                    vector = embed_text(client, row.embedding_text)
                    new_embedding = ResaleTransactionsEmbeddings(
                        transaction_id = row_id,
                        embedding = vector,
                        embedding_model = OLLAMA_MODEL
                    )
                    session.add(new_embedding)
                    success_count += 1
                except Exception as e:
                    logger.warning(f"Failed to embed row id={row_id}: {e}")
                    failure_count += 1
                finally:
                    # Increment row counter regardless of error so the UI stays synced
                    pbar.update(1)
            
                if idx % COMMIT_EVERY == 0:
                    session.commit()
                    session.expunge_all()

            # Final partial batch
            session.commit()
            session.expunge_all()

        logger.info(f"Done. Success: {success_count:,}, Failed: {failure_count:,}")
    finally:
        session.close()


    #     for idx, row in enumerate(tqdm(iter_unembedded(session, COMMIT_EVERY), 
    #                                    total=total_remaining), start=1):
    #         row_id = row.id
    #         try:
    #             vector = embed_text(client, row.embedding_text)
    #             new_embedding = ResaleTransactionsEmbeddings(
    #                 transaction_id = row_id,
    #                 embedding = vector,
    #                 embedding_model = OLLAMA_MODEL
    #             )
    #             session.add(new_embedding)
    #             success_count += 1
    #         except Exception as e:
    #             logger.warning(f"Failed to embed row id={row.id}: {e}")
    #             failure_count += 1
    #             continue   

    #         if idx % COMMIT_EVERY == 0:
    #             session.commit()
    #             session.expunge_all()
    #             #logger.info(f"Committed batch at row {idx:,}")

    #     session.commit()
    #     session.expunge_all()
    #     logger.info(
    #         f"Done. Success: {success_count:,}, Failed: {failure_count:,}"
    #     )
    # finally:
    #     session.close()


if __name__ == "__main__":
    main()
