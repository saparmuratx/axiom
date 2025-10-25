import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.models.model_mixins import BaseModelMixin, SerializerMixin, AsyncEagerLoadingMixin
from axiom.models.base import AsyncBase


Base = AsyncBase


class Chapter(Base, BaseModelMixin, AsyncEagerLoadingMixin, SerializerMixin):
    __tablename__ = "chapters"

    # Columns
    book_id: Mapped[uuid.UUID] = mapped_column()
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    prev_chapter: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chapters.id"), nullable=True)
    next_chapter: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chapters.id"), nullable=True)

    chunks: Mapped[list["Chunk"]] = relationship("Chunk", back_populates="chapter", cascade="all, delete")

    prev: Mapped["Chapter"] = relationship("Chapter", remote_side="Chapter.id", foreign_keys=[prev_chapter], post_update=True)
    next: Mapped["Chapter"] = relationship("Chapter", remote_side="Chapter.id", foreign_keys=[next_chapter], post_update=True)


class Chunk(Base, BaseModelMixin, AsyncEagerLoadingMixin, SerializerMixin):
    __tablename__ = "chunks"

    chapter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"))
    size: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    prev_chunk: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chunks.id"), nullable=True)
    next_chunk: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chunks.id"), nullable=True)

    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="chunks")
    prev: Mapped["Chunk"] = relationship("Chunk", remote_side="Chunk.id", foreign_keys=[prev_chunk], post_update=True)
    next: Mapped["Chunk"] = relationship("Chunk", remote_side="Chunk.id", foreign_keys=[next_chunk], post_update=True)
