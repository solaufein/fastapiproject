"""Services module."""
import logging
from typing import List
from uuid import uuid4

from fastapiproject.repositories.user_repository import UserRepository
from fastapiproject.api.models import UserDto

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> List[UserDto]:
        users = self._repository.get_all()
        user_dtos = [UserDto(id=user.id, name=user.name) for user in users]
        return user_dtos

    def get_user_by_id(self, user_id: int) -> UserDto:
        logger.info(f"Get user by id: {user_id}")

        user = self._repository.get_by_id(user_id)
        return UserDto(id=user.id, name=user.name)

    def create_user(self) -> UserDto:
        uid = uuid4()
        user = self._repository.add(name=f"{uid}@email.com")
        return UserDto(id=user.id, name=user.name)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
