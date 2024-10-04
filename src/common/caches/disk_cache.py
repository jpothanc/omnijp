import logging
from abc import abstractmethod


class DiskCache:
    def __init__(self, cache_dir, cache_name, can_zip=False, rows_per_file=1000000):
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.rows_per_file = rows_per_file
        self.can_zip = can_zip
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def save(self, header, data):
        pass
