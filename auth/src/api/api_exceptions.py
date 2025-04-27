from fastapi.exceptions import HTTPException
from fastapi import status


def make_not_found(resource: str = "Resource"):
    return HTTPException(
        detail={"detail": f"{resource.title()} not found"},
        status_code=status.HTTP_404_NOT_FOUND,
    )
