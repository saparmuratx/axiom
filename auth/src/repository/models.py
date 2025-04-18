from typing import Any, Optional, List, Dict

from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, UUID
from sqlalchemy.dialects.postgresql import JSONB

from src.repository.mixins import BaseModelMixin, SerializerMixin
from src.config import settings


class Base(DeclarativeBase):
    pass


class User(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=False) 

    role_id = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    profile: Mapped["Profile"] = relationship(back_populates="user")


class Profile(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "profiles"

    firs_tname: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="profile", single_parent=True)
    
    __table_args__ = (UniqueConstraint("user_id"),)


class Role(Base, BaseModelMixin, SerializerMixin):
    __tablename__ = "roles"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text())
    permissions: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")


if __name__ == "__main__":
    from src.config import settings
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    import random

    engine = create_engine(settings.DATABASE_URL)

    with Session(engine) as session:
        email = f"some{random.randint(1000, 9999)}@mail.com"
        password = str(random.randint(10000000, 99999999))

        # user = User(email=email,password=password)  

        # role = Role(title="admin", description="Admin Role", permissions={"auth:user": {"create":True, "read":True, "update": True, "delete": True}})

        # user.role = role

        # session.add(user)
        # session.add(role)

        # session.commit()

        user = session.query(User).filter().first()


        # for user in users:
        print(user.to_dict(), end="\n\n")
        print(user.role.to_dict())
