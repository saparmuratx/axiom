from passlib.context import CryptContext



class PasswordService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, raw_password: str, hashed_password: str):
        return self.context.verify(secret=raw_password, hash=hashed_password)

    def get_password_hash(self, raw_password):
        return self.context.hash(secret=raw_password)
