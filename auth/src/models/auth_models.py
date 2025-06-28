from typing import Any, Dict

from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped, Session
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, UUID, event
from sqlalchemy.dialects.postgresql import JSONB

from src.repository.unit_of_work import get_session
from src.models.model_mixins import BaseModelMixin, SerializerMixin


class Base(DeclarativeBase):
    pass


class User(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        passive_deletes=True,
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=False,
    )


class Profile(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)

    avatar: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="profile", single_parent=True)

    __table_args__ = (UniqueConstraint("user_id"),)


class Role(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "roles"

    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text())
    permissions: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


def init_roles(session: Session):
    admin_role = Role(title="admin", description="Site administrator", permissions={})

    moderator_role = Role(
        title="moderator", description="Site moderator", permissions={}
    )

    user_role = Role(title="user", description="Regular user", permissions={})

    session.add_all([admin_role, moderator_role, user_role])

    session.commit()


if __name__ == "__main__":
    init_roles(next(get_session()))
