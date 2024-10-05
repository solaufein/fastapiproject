"""Containers module."""

import logging.config

from dependency_injector import containers, providers

from .db.database import Database
from .db.repositories import UserRepository
from .logging_config import get_logging_config
from .services import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".api.endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.config.dictConfig,
        config=get_logging_config(),
    )

    db = providers.Singleton(
        Database,
        db_url=config.db.url,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )
