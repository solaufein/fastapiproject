import logging
import time
import uuid
from multiprocessing import Pool

logger = logging.getLogger(__name__)


class WorkerService:

    def __init__(self, worker_pool: Pool) -> None:
        self.worker_pool: Pool = worker_pool

    def start_task(self, a: int, b: int):
        task_id = str(uuid.uuid4())

        self.worker_pool.apply_async(
            WorkerService.heavy_task,
            args=(task_id, a, b),
            callback=lambda result: WorkerService.task_callback(task_id, result)
        )

        return {"task_id": task_id}

    def task_status(self, task_id: str):
        return 'in-progress'

    @staticmethod
    def heavy_task(task_id, a, b):
        logger.info(f"Starting Task {task_id} with params: {a}, {b}")
        time.sleep(5)
        return a * b

    @staticmethod
    def task_callback(task_id, result):
        """Callback to update task status after completion."""
        logger.info(f"Task {task_id} completed with result: {result}")
