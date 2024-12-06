import logging.config
from multiprocessing import Pool

from dependency_injector import containers, providers

from fastapiproject.db.database import Database
from fastapiproject.repositories.user_repository import UserRepository
from fastapiproject.services.user_service import UserService
from .logging_config import get_logging_config


def init_worker_pool(workers: int):
    pool = Pool(workers)
    yield pool
    pool.close()
    pool.join()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["fastapiproject.api.endpoints"])

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

    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository
    )

    worker_pool = providers.Resource(
        init_worker_pool,
        workers=4
    )
