from typing import Optional, List

from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, String

from src.repository.mixins import BaseModelMixin
from src.config import settings


class Base(DeclarativeBase):
    pass


class Account(Base, BaseModelMixin):
    __tablename__ = "accounts"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)


if __name__ == "__main__":
    from src.config import settings
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    import random

    print(settings.DATABASE_URL)

    engine = create_engine(settings.DATABASE_URL)

    with Session(engine) as session:
        
        email = f"some{random.randint(1, 99)}@mail.com"

        account = Account(email=email)

        session.add(account)

        session.commit()
 