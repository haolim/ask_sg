# Layer 3: DB table shape (SQLAlchemy)
# ORM Layer 3
# Direct 1-to-1 mapping of DB table. 
# SQLAlchemy. No API knowledge

from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ask_sg.core.database import Base


class ResaleTransactions(Base):
    __tablename__ = "resale_transactions"


    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    town: Mapped[str] = mapped_column()
    block: Mapped[str] = mapped_column()
    flat_type: Mapped[str] = mapped_column()
    street_name: Mapped[str] = mapped_column()
    storey_range: Mapped[str] = mapped_column()
    floor_area_sqm: Mapped[int] = mapped_column()
    flat_model: Mapped[str] = mapped_column()
    lease_commence_year: Mapped[int] = mapped_column()
    resale_price: Mapped[int] = mapped_column()
    sold_year: Mapped[int] = mapped_column()
    sold_month: Mapped[int] = mapped_column()
    remaining_lease_year: Mapped[int] = mapped_column()
    remaining_lease_month: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    #TODO: Move embedding_text to resale_transactions_embeddings table
    embedding_text: Mapped[str] = mapped_column()

    # Relationship to ResaleTransactionsEmbedding - One-to-Many (one transaction has MANY embeddings)
    embeddings: Mapped[list["ResaleTransactionsEmbeddings"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")