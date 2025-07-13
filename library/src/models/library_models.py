import uuid
from datetime import date

from xmlrpc.client import Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.types import String, UUID

from axiom.models.model_mixins import BaseModelMixin, SerializerMixin, AsyncEagerLoadingSerailizerAlternativeMixin
from axiom.models.base import AsyncBase


Base = AsyncBase


class Book(Base, BaseModelMixin, AsyncEagerLoadingSerailizerAlternativeMixin):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column()
    published_at: Mapped[date] = mapped_column()

    edition: Mapped[str] = mapped_column(String(255))

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE")
    )
    author: Mapped["Author"] = relationship("Author", back_populates="books")

    genres: Mapped[list["Genre"]] = relationship(
        "Genre", secondary="book_genre", back_populates="books"
    )
    collections: Mapped[list["Collection"]] = relationship(
        "Collection", secondary="book_collection", back_populates="books"
    )

    notes: Mapped[list["Note"]] = relationship("Note", back_populates="book")
    highlights: Mapped[list["Highlight"]] = relationship(
        "Highlight", back_populates="book"
    )
    reading_progresses: Mapped[list["ReadingProgress"]] = relationship(
        "ReadingProgress", back_populates="book"
    )


class Author(Base, BaseModelMixin, AsyncEagerLoadingSerailizerAlternativeMixin):
    __tablename__ = "authors"

    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pseudonym: Mapped[str | None] = mapped_column(String(255), nullable=True)

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Genre(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "genres"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary="book_genre", back_populates="genres"
    )


class BookGenre(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "book_genre"

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))
    genre_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("genres.id"))


class Collection(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "collections"

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    user_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    is_public: Mapped[Boolean] = mapped_column(default=False)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary="book_collection", back_populates="collections"
    )


class BookCollection(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "book_collection"

    collection_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collections.id"))
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))


class Favorites(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "favorites"

    user_id: Mapped[uuid.UUID] = mapped_column()
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="unique_together_user_book"),
    )


class Note(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "notes"

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[uuid.UUID] = mapped_column()
    chapter_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    chunk_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    offset_start: Mapped[int] = mapped_column(nullable=True)
    offset_end: Mapped[int] = mapped_column(nullable=True)
    note_text: Mapped[str] = mapped_column()

    book: Mapped["Book"] = relationship(back_populates="notes")


class Highlight(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "highlights"

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[uuid.UUID] = mapped_column()
    chapter_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    chunk_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    offset_start: Mapped[int] = mapped_column(nullable=True)
    offset_end: Mapped[int] = mapped_column(nullable=True)
    book: Mapped["Book"] = relationship(back_populates="highlights")


class ReadingProgress(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "reading_progresses"

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[uuid.UUID] = mapped_column()
    chapter_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    chunk_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    offset: Mapped[int] = mapped_column(nullable=True)
    book: Mapped["Book"] = relationship(back_populates="reading_progresses")
