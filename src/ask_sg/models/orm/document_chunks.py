from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4
from datetime import datetime
from ask_sg.core.database import Base


class DocumentChunks(Base):
    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_agency: Mapped[str] = mapped_column()
    source_url: Mapped[str | None] = mapped_column()
    document_title: Mapped[str | None] = mapped_column()
    document_category: Mapped[str | None] = mapped_column()
    chunk_index: Mapped[int] = mapped_column()
    chunk_text: Mapped[str] = mapped_column()
    embedding_text: Mapped[str| None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship to DocumentChunksEmbeddings: One-to-Many (one embedding text chunk has many embeddings)
    embeddings: Mapped[list["DocumentChunksEmbeddings"]] = relationship(back_populates="doc_chunk", cascade="all, delete-orphan")