
from dataclasses import dataclass


@dataclass
class TableInfo:
    name: str
    row_count: int
    time_taken: float

class DBCacheResults:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.host_name = None
        self.tables_cached = 0
        self.tables:list[TableInfo] = []

    