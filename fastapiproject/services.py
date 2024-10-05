"""Services module."""
import logging

logger = logging.getLogger(__name__)


class SearchService:

    def __init__(self):
        self.users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Max"},
        ]

    def get_user_by_id(self, user_id: int):
        logger.info(f"Get user by id: {user_id}")

        for user in self.users:
            if user["id"] == user_id:
                return user
        return None
