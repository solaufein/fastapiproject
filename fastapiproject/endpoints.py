"""Endpoints module."""
import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi import HTTPException

from fastapiproject.services import SearchService
from .containers import Container
from .model.models import User

router = APIRouter()

logger = logging.getLogger(__name__)


# Route for healthcheck (filtered out from uvicorn logging)
@router.get("/healthcheck")
async def healthcheck():
    return {"status": "up"}


# Route that intentionally raises an HTTPException
@router.get("/error-http")
@inject
async def read_root(search_service: SearchService = Depends(Provide[Container.search_service]), ):
    raise HTTPException(status_code=400, detail=f"This is a bad request.")


# Route that raises a generic exception
@router.get("/error-generic")
@inject
async def read_generic_error(search_service: SearchService = Depends(Provide[Container.search_service]), ):
    raise ValueError(f"An unexpected error occurred!")


# Route that runs successfully
@router.get("/users/{user_id}", response_model=User, response_model_exclude_unset=True)
@inject
async def get_user(user_id: int, search_service: SearchService = Depends(Provide[Container.search_service]), ) -> User:
    result = search_service.get_user_by_id(user_id)
    logger.info(f"User: {result}")

    return result
