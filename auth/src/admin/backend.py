from starlette_admin.contrib.sqla import Admin, ModelView

from sqlalchemy import create_engine

from src.config import settings
from src.models.auth_models import User, Profile, Role

from src.repository.unit_of_work import get_session
from src.repository.user_repository import UserRepository

from src.services.password_service import PasswordService
from src.admin.auth_provider import UsernameAndPasswordProvider

session = next(get_session())

user_repository = UserRepository(session=session)
password_service = PasswordService()

engine = create_engine(settings.DATABASE_URL)

admin = Admin(
    engine=engine,
    title="Axiom AUTH Admin",
    auth_provider=UsernameAndPasswordProvider(
        user_repository=user_repository,
        password_service=password_service,
    ),
)

admin.add_view(ModelView(Role))
admin.add_view(ModelView(User))
admin.add_view(ModelView(Profile))
