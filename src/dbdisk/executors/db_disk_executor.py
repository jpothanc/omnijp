import logging
import os
from abc import abstractmethod

from src.dbdisk.db_disk_request import DbDiskRequest
from src.dbdisk.db_disk_result import DbDiskResult


class DbDiskExecutor:

    def __init__(self, db_disk_request: DbDiskRequest):
        self.db_disk_request = db_disk_request
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def execute(self) -> DbDiskResult:
        pass

    @property
    def _thread_workers(self):
        return min(5, os.cpu_count() + 4)
