"""Endpoints module."""
import logging
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi import HTTPException
from starlette import status

from fastapiproject.services.user_service import UserService
from fastapiproject.core.containers import Container
from fastapiproject.repositories.user_repository import NotFoundError
from fastapiproject.api.models import UserDto

router = APIRouter(prefix="/fastapi")

logger = logging.getLogger(__name__)


# Route for healthcheck (filtered out from uvicorn logging)
@router.get("/healthcheck")
async def healthcheck():
    return {"status": "up"}


# Route that intentionally raises an HTTPException
@router.get("/error-http")
@inject
async def read_root(user_service: UserService = Depends(Provide[Container.user_service]), ):
    raise HTTPException(status_code=400, detail=f"This is a bad request.")


# Route that raises a generic exception
@router.get("/error-generic")
@inject
async def read_generic_error(user_service: UserService = Depends(Provide[Container.user_service]), ):
    raise ValueError(f"An unexpected error occurred!")


# Routes that runs successfully
@router.get("/users/{user_id}", response_model=UserDto, response_model_exclude_unset=True)
@inject
async def get_user(user_id: int, user_service: UserService = Depends(Provide[Container.user_service]), ):
    try:
        result = user_service.get_user_by_id(user_id)
        logger.info(f"User: {result}")
        return result
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/users", response_model=List[UserDto])
@inject
async def get_list(user_service: UserService = Depends(Provide[Container.user_service]), ):
    return user_service.get_users()


@router.post("/users", response_model=UserDto, status_code=status.HTTP_201_CREATED)
@inject
async def add(user_service: UserService = Depends(Provide[Container.user_service]), ):
    return user_service.create_user()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove(user_id: int, user_service: UserService = Depends(Provide[Container.user_service]), ):
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
