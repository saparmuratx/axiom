import logging
from typing_extensions import Annotated, Doc

from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.security import SecurityScopes

from axiom.services.jwt_service import JWTService

logger = logging.getLogger(__name__)


class JWTBearerAuthentication:
    def __init__(
        self,
        jwt_service: Annotated[
            JWTService,
            Doc(
                """
                    Instance of `axiom.services.jwt_service.JWTService`. 
                    Used for validation JWT Bearer Token.
                """
            ),
        ],
        aud: Annotated[
            str,
            Doc(
                """ 
                    `aud` for validating JWT Bearer Token audience(domain).
                """
            ),
        ],
    ):
        self.jwt_service = jwt_service
        self.aud = aud

    async def __call__(self, request: Request, security_scopes: SecurityScopes) -> str:
        bearer_token = request.headers.get("Authorization", "")

        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        if not bearer_token or not bearer_token.startswith("Bearer "):
            request.state.user_id = None
            request.state.scope = "guest"

        else:
            try:
                token = bearer_token.split(" ")[1].strip()
                token_payload = self.jwt_service.validate_token(
                    token=token, aud=self.aud
                )

                request.state.user_id = token_payload["sub"]
                request.state.scope = token_payload.get("scope", "user")

            except Exception as e:
                logger.error(str(e))
                raise credentials_exception

        if security_scopes.scopes and request.state.scope not in security_scopes.scopes:
            logger.error(
                f"Not enough permissions for User(id={request.state.user_id}) with scope={request.state.scope}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

        return request.state.user_id
