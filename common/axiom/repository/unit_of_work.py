from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class UnitOfWork:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def __enter__(self):
        session =  Session(create_engine(self.database_url))        
        
        self.session = session
        
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
