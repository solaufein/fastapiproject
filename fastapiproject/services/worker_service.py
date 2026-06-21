import asyncio
import logging
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor

logger = logging.getLogger(__name__)


class WorkerService:

    def __init__(self, worker_pool: ThreadPoolExecutor) -> None:
        self.worker_pool = worker_pool

    async def task_status(self, task_id: str):
        return 'in-progress'

    def start_task(self, a: int, b: int) -> asyncio.Future[int]:
        task_id = str(uuid.uuid4())

        sync_future = self.worker_pool.submit(
            WorkerService.heavy_task,
            task_id, a, b,
        )
        sync_future.add_done_callback(
            lambda future: WorkerService.task_callback(task_id, future)
        )

        return asyncio.wrap_future(sync_future)

    @staticmethod
    def heavy_task(task_id, a, b):
        logger.info(f"Starting Task {task_id} with params: {a}, {b}")
        time.sleep(5)
        return a * b

    @staticmethod
    def task_callback(task_id: str, future: Future):
        try:
            result = future.result()
            logger.info(f"Task {task_id} completed successfully with result: {result}")
        except Exception as exc:
            logger.error(f"Task {task_id} failed with exception: {exc}", exc_info=True)
