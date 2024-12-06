import logging
import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import partial

logger = logging.getLogger(__name__)


class WorkerService:

    def __init__(self, worker_pool: ProcessPoolExecutor) -> None:
        self.worker_pool: ProcessPoolExecutor = worker_pool

    def start_task(self, a: int, b: int):
        task_id = str(uuid.uuid4())

        task_future = self.worker_pool.submit(
            WorkerService.heavy_task,
            task_id, a, b,
        )
        callback_with_task_id = partial(WorkerService.task_callback, task_id)
        task_future.add_done_callback(callback_with_task_id)

        return task_id

    def task_status(self, task_id: str):
        return 'in-progress'

    @staticmethod
    def heavy_task(task_id, a, b):
        logger.info(f"Starting Task {task_id} with params: {a}, {b}")
        time.sleep(5)
        return a * b

    @staticmethod
    def task_callback(task_id, future):
        result = future.result()
        logger.info(f"Task {task_id} completed with result: {result}")
