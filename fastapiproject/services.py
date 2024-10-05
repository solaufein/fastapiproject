"""Services module."""
import logging

from fastapi import HTTPException

from fastapiproject.model.models import User

logger = logging.getLogger(__name__)


class SearchService:

    def __init__(self):
        self.users = {
            1: User(id=1, name="Alice"),
            2: User(id=2, name="Bob"),
            3: User(id=3, name="Max"),
        }

    def get_user_by_id(self, user_id: int) -> User | None:
        logger.info(f"Get user by id: {user_id}")

        user = self.users.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return user
