# Repositories Layer 5
# All DB queries live here.
# Talks to ORM.
# No business logic, no HTTP

from sqlalchemy.orm import Session
from sqlalchemy import select
from ask_sg.models.orm.resale_transactions import ResaleTransactions
from ask_sg.models.orm.resale_transactions_embeddings import ResaleTransactionsEmbeddings
from collections.abc import Sequence

def get_embedding_rows(
        session: Session, 
        embedding_model: str,
        query_vector: list[float],
        limit: int = 10
        ) -> Sequence[str] : # annotate with the narrowest type. since we don't need 
                        # to mutate this, we just use the narrowest Sequence without 
                        # converting it to a list
    distance = ResaleTransactionsEmbeddings.embedding.cosine_distance(query_vector).label("distance")
    stmt = (
        select(
            ResaleTransactionsEmbeddings.embedding_text
        )
        .join(
            ResaleTransactions,
            ResaleTransactionsEmbeddings.transaction_id == ResaleTransactions.id
        )
        .where(
            ResaleTransactionsEmbeddings.embedding_model == embedding_model
        )
        .order_by(distance)
        .limit(limit)
    )
    return session.scalars(stmt).all() # scalars will reutrn a list of strings