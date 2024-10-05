import json
import socket
from dataclasses import asdict, dataclass, field

from src.common.helper import getcurrenttime


@dataclass
class TableResult:
    name: str
    row_count: int
    # ignore header and data when converting to dict
    header: list = field(default_factory=list)
    data: list = field(default_factory=list)
    time_taken: str = ""

    # def to_dict(self):
    #     return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if k not in ['header', 'data']})

    def to_dict(self):
        # Convert the dataclass to a dictionary
        full_dict = asdict(self)

        # Create a new dictionary excluding 'header' and 'data'
        filtered_dict = {}
        for key, value in full_dict.items():
            if key not in ['header', 'data']:
                filtered_dict[key] = value

        return filtered_dict


class DbResult:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.host_name: str = socket.gethostname()
        self.total_tables: int = 0
        self.total_rows: int = 0
        self.tables: list[TableResult] = []

    def set_start_time(self):
        self.start_time = getcurrenttime()

    def set_end_time(self):
        self.end_time = getcurrenttime()

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
            "total_rows": self.total_rows,
            "tables": [table.to_dict() for table in self.tables]
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
