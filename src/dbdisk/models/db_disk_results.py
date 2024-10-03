
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import socket


@dataclass
class TableInfo:
    name: str
    row_count: int
    time_taken: str = ""


@dataclass
class DbDiskResults:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    def __init__(self):
        self.start_time = None
        self.end_time = None
        # self.elapsed_time:str = ""
        self.host_name:str = socket.gethostname()
        self.total_tables_dumped: int = 0
        self.total_rows_dumped: int = 0
        self.tables:list[TableInfo] = []

    def set_start_time(self):
        self.start_time =  datetime.now().strftime(self.DATETIME_FORMAT)[:-3]

    def set_end_time(self):
        self.end_time =  datetime.now().strftime(self.DATETIME_FORMAT)[:-3]

    
    def add_table(self, table_info: TableInfo):
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
            "tables": [asdict(table) for table in self.tables]
    }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)