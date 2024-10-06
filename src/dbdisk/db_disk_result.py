
from dataclasses import asdict, dataclass
import json
import socket

from src.common.constants import DATETIME_FORMAT
from src.common.helper import getcurrenttime


@dataclass
class TableDumpResult:
    name: str
    row_count: int
    time_taken: str = ""


@dataclass
class DbDiskResult:
    start_time = None
    end_time = None
    host_name = socket.gethostname()
    total_tables_dumped = 0
    total_rows_dumped = 0
    total_chunks_dumped = 0
    tables = []

    def set_start_time(self):
        self.start_time =  getcurrenttime()

    def set_end_time(self):
        self.end_time =  getcurrenttime()

    
    def add_table(self, table_info: TableDumpResult):
        self.tables.append(table_info)
        self.total_tables_dumped += 1
        self.total_rows_dumped += table_info.row_count
    
    def __str__(self) -> str:
        return f"DbDiskResults: {vars(self)}"
    
    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "host_name": self.host_name,
            "total_tables_dumped": self.total_tables_dumped,
            "total_rows_dumped": self.total_rows_dumped,
            "total_chunks_dumped": self.total_chunks_dumped,
            "tables": [asdict(table) for table in self.tables]
    }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)