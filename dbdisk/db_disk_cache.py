from abc import ABC, abstractmethod


class DbDiskCache:
    def __init__(self, cache_dir, cache_name):
        self.cache_dir = cache_dir
        self.cache_name = cache_name

    @abstractmethod
    def save(self, header, data):
        pass
