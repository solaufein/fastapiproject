import logging
import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import partial

logger = logging.getLogger(__name__)


class WorkerService:
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   Standalone Functions vs. @staticmethod vs. partial:
    #       Use 'standalone functions' when tasks don't need to access any shared state or instance-specific data.
    #       Use @staticmethod if tasks logically belongs to a class but doesn't depend on instance-specific state (self).
    #       Use 'partial' to bind additional context or dependencies dynamically e.g. DB session
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   For SQLAlchemy or Other Shared Resources:
    #       Use ProcessPoolExecutor's 'initializer' to set up shared resources per process if needed.
    #       Alternatively, explicitly pass resources to the task via 'partial'.
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   Issue with 'self' using Pool/Process:
    #       The issue arises because multiprocessing.
    #       Pool creates separate processes, and when you pass instance methods like self.heavy_task or self.task_callback,
    #       those methods rely on the instance state (self).
    #       However, in a new process, the instance (self) does not exist because Python does not serialize instance methods by default.
    #       Instead, only static or top-level functions are safely pickled and sent to the worker processes.
    #       When you pass self.heavy_task or self.task_callback to apply_async, the multiprocessing library attempts to pickle the method.
    #       This process fails or results in unexpected behavior because the bound method (self.method) ties to the current process's memory
    #       and is not transferable to another process.
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __init__(self, worker_pool: ProcessPoolExecutor) -> None:
        self.worker_pool = worker_pool

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
