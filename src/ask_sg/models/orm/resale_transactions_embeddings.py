from sqlalchemy import func, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4
from datetime import datetime
from pgvector.sqlalchemy import Vector
from ask_sg.core.database import Base
from sqlalchemy import Index

class ResaleTransactionsEmbeddings(Base):
    __tablename__ = "resale_transactions_embeddings"
    __table_args__ = (
        UniqueConstraint(
            "transaction_id",
            "embedding_model",
            name="uq_transaction_model"
        ),
        Index("idx_embeddings_hnsw", "embedding", postgresql_using="hnsw", 
              postgresql_ops={"embedding": "vector_cosine_ops"},
              ),
        # trailing comma required to make this a tuple
    )
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    transaction_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("resale_transactions.id"))
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768))
    embedded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    embedding_model: Mapped[str] = mapped_column()
    embedding_text: Mapped[str] = mapped_column()

    # Relationship to ResaleTransactions - Many-to-one (this embedding belongs to ONE transaction)
    transaction: Mapped["ResaleTransactions"] = relationship(back_populates="embeddings")