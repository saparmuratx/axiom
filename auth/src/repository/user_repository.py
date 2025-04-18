from sqlalchemy.orm import Session

from src.repository.models import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    
    def get_by_id(self, id: str):

        user = self.session.query(User).filter(User.id==id).first()

        return user.to_dict()
    
    def get(self, id):

        return self.get_by_id(id)
    
    def list(self, )