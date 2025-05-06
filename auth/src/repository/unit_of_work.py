from src.utils.debug_print import debug_print
from src.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def get_session():
    with Session(create_engine(settings.DATABASE_URL)) as session:
        yield session


class UnitOfWork:
    def __init__(self):
        self.session_maker = get_session

    def __enter__(self):
        self.session = next(self.session_maker())

        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            self.rollback()
            self.session.close()

        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
