from dataclasses import asdict, dataclass
import json
import socket
from datetime import datetime

from src.common.constants import DATETIME_FORMAT
from src.common.helper import getcurrenttime

@dataclass
class TableResult:
    name: str
    row_count: int
    header: list
    data:   list
    time_taken: str = ""
    
class DbResult:
     def __init__(self):
            self.start_time = None
            self.end_time = None
            self.host_name:str = socket.gethostname()
            self.total_tables: int = 0
            self.total_rows: int = 0
            self.tables:list[TableResult] = []

     def set_start_time(self):
        self.start_time =  getcurrenttime()

     def set_end_time(self):
        self.end_time =  getcurrenttime()

     def add_table(self, table_result: TableResult):
        self.tables.append(table_result)
        self.total_tables += 1
        self.total_rows += table_result.row_count

     def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "host_name": self.host_name,
            "total_tables": self.total_tables,
            "total_rows": self.total_rows
        }

     def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)