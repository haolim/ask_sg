from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4
from datetime import datetime
from pgvector.sqlalchemy import Vector
from ask_sg.core.database import Base

class DocumentChunksEmbeddings(Base):
    __tablename__ = "document_chunks_embeddings"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    chunk_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("document_chunks.id"))
    document_chunk_embedding: Mapped[list[float] | None] = mapped_column(Vector(768))
    embedding_model: Mapped[str] = mapped_column()
    embedded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship - Many-to-One
    doc_chunk: Mapped["DocumentChunks"] = relationship(back_populates="embeddings")