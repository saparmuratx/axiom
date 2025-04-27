from typing import Any
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.schemas.profile_schemas import ProfileUpdateSchema
from src.repository.repository_exceptions import NotFoundException
from src.repository.unit_of_work import UnitOfWork
from src.repository.profile_repository import ProfileRepository

from src.services.profile_service import ProfileService

from src.api.api_exceptions import make_not_found

profiles_router = APIRouter(tags=["Profiles"])


@profiles_router.get("/profiles")
def list_profiles(**filters: dict[str, Any]):
    try:
        with UnitOfWork() as unit_of_work:
            profile_repository = ProfileRepository(unit_of_work.session)

            profile_service = ProfileService(profile_repository)

            profiles = profile_repository.list()

        return profiles

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@profiles_router.get("/profiles/{profile_id}")
def retrieve_profile(profile_id: str):
    try:
        with UnitOfWork() as unit_of_work:
            profile_repository = ProfileRepository(unit_of_work.session)
            profile_service = ProfileService(profile_repository)

            profile = profile_service.get_profile(profile_id)

        return profile

    except NotFoundException as e:
        raise make_not_found("Profile")


@profiles_router.patch("/profiles/{profile_id}")
def update_profile(profile_id: str, data: ProfileUpdateSchema):
    try:
        with UnitOfWork() as unit_of_work:
            profile_repository = ProfileRepository(unit_of_work.session)
            profile_service = ProfileService(profile_repository)

            profile = profile_service.update_profile(profile_id, data)

        return profile
    except NotFoundException as e:
        raise make_not_found("Profile")
