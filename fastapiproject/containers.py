"""Containers module."""

import logging.config

from dependency_injector import containers, providers

from . import services
from .logging_config import get_logging_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.config.dictConfig,
        config=get_logging_config(),
    )

    search_service = providers.Factory(
        services.SearchService,
    )
