from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider, AdminUser, AdminConfig, BaseAuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.repository.repository_exceptions import NotFoundException
from src.repository.user_repository import UserRepository

from src.services.password_service import PasswordService


class UsernameAndPasswordProvider(AuthProvider):
    def __init__(
        self, user_repository: UserRepository, password_service: PasswordService
    ):
        super().__init__()
        self.user_repository = user_repository
        self.password_service = password_service

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        # Fetch user by email or username (adjust based on your UserRepository)
        try:
            user = self.user_repository.get_by_email(username)  # Or get_by_username
        except NotFoundException as e:
            raise LoginFailed("Invalid username or password")

        if not user or user.role.title != "admin":
            raise LoginFailed("Invalid username or password")

        if not user.is_active:
            raise LoginFailed("Account is inactive")

        # Verify password using PasswordService
        if not self.password_service.verify_password(password, user.password):
            raise LoginFailed("Invalid username or password")

        # Store user ID or email in session
        request.session.update(
            {"username": user.email, "remember_me": remember_me}
        )  # Or user.id
        return response

    async def is_authenticated(self, request: Request) -> bool:
        username = request.session.get("username")
        if username:
            user = self.user_repository.get_by_email(username)  # Or get_by_username
            if user and user.is_active:
                request.state.user = {
                    "name": user.profile.first_name,  # Adjust based on user model
                    "role": user.role.title,
                    "avatar": user.profile.avatar,
                }
                return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user
        custom_app_title = f"Hello, {user['name']}!"
        custom_logo_url = user.get("avatar")

        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        photo_url = user.get("avatar")
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
