from fastapi.exceptions import HTTPException
from fastapi import status


def make_not_found(resource: str = "Resource"):
    return HTTPException(
        detail={"detail": f"{resource.title()} not found"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active"
        )


class IncorrectOldPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
        )
