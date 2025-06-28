from starlette import status
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from pydantic_settings import BaseSettings

from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from axiom.service.jwt_service import JWTService
from axiom.debug_utils import debug_print


class JWTAuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: BaseSettings, dispatch=None, aud: list[str] = None, jwt_service: JWTService = None):
        super().__init__(app, dispatch)
        self.aud = aud
        self.settings = settings
        self.jwt_service = jwt_service

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        debug_print(request=request, request_url_path=request.url.path)

        if not self.settings.AUTH_ON:
            request.state.user_id = "test"

            return await call_next(request)

        if request.url.path.strip("/") in ["docs", "openapi.json"]:
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        debug_print(self_aud=self.aud)

        bearer_token = request.headers.get("Authorization")

        if request.url.path.startswith(
            (
                "/admin",
                "/admin/",
                "/auth/login",
                "/auth/register",
                "/favicon.ico",
            )
        ):
            return await call_next(request)

        debug_print(bearer_token=bearer_token)

        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing access token"},
            )
        try:
            token = bearer_token.split(" ")[1].strip()
            debug_print(token=token)

            token_payload = self.jwt_service.validate_token(token=token, aud=self.aud)
            debug_print(token_payload=token_payload)
        except (
            ValueError,
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as e:
            debug_print(exception_type=type(e))

            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(e)},
            )
        else:
            request.state.user_id = token_payload["sub"]

        return await call_next(request)
