import logging
import uuid

from sqlalchemy import event, ForeignKey, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.models.model_mixins import (
    BaseModelMixin,
    SerializerMixin,
    AsyncEagerLoadingMixin,
)
from axiom.models.base import AsyncBase


Base = AsyncBase

logger = logging.getLogger(__name__)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


# TODO: fix relationships
class Chapter(Base, BaseModelMixin, AsyncEagerLoadingMixin, SerializerMixin):
    __tablename__ = "chapters"

    book_id: Mapped[uuid.UUID] = mapped_column()
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    prev_chapter: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("chapters.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk", back_populates="chapter", cascade="all, delete"
    )

    prev: Mapped["Chapter"] = relationship(back_populates="next")

    next: Mapped["Chapter"] = relationship(
        "Chapter",
    )


# TODO: fix relationships
class Chunk(Base, BaseModelMixin, AsyncEagerLoadingMixin, SerializerMixin):
    __tablename__ = "chunks"

    chapter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE")
    )
    size: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)

    prev_chunk: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("chunks.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="chunks")
    # prev: Mapped["Chunk"] = relationship(
    #     "Chunk",
    #     remote_side="Chunk.id",
    #     back_populates="next_chapter",
    #     foreign_keys=[prev_chunk],
    #     post_update=True,
    # )
    # next: Mapped["Chunk"] = relationship(
    #     "Chunk",
    #     remote_side="Chunk.id",
    #     # back_populates="prev_chapter",
    #     viewonly=True,
    # )
