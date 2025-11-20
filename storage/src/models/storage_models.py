import logging
import uuid
from datetime import datetime

from sqlalchemy import event, ForeignKey, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import object_session

from axiom.models.model_mixins import BaseModelMixin, SerializerMixin, AsyncEagerLoadingMixin
from axiom.models.base import AsyncBase


Base = AsyncBase

logger = logging.getLogger(__name__)

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

@event.listens_for(Chapter.prev, "set", propagate=True)
def sync_next_chapter(target, value, oldvalue, initiator):
    print(f"SET PREVIOUS for chapter {Chapter.id} {Chapter.prev}")
    if value is not None:
        value.next = target

# @event.listens_for(Chapter.next, "set", propagate=True)
# def sync_prev_chapter(target, value, oldvalue, initiator):
#     if value is not None:
#         value.next = target

# @event.listens_for(Chunk.prev, "set", propagate=True)
# def sync_next_chunk(target, value, oldvalue, initiator):
#     if value is not None:
#         value.next = target

# @event.listens_for(Chunk.next, "set", propagate=True)
# def sync_prev_chunk(target, value, oldvalue, initiator):
#     if value is not None:
#         value.next = target

@event.listens_for(Chapter, "after_insert")
def before_insert(mapper, connection, target):
    logger.debug(f"MAPPER: {mapper}")
    logger.debug(f"CONNECTION: {connection}")
    logger.debug(f"TARGET: {target}")

    logger.info(target.to_dict())

    if target.prev:
        target.prev.next = target
    if target.next:
        target.next.prev = target

    

    