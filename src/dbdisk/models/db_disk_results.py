
from dataclasses import dataclass


@dataclass
class TableInfo:
    name: str
    row_count: int
    time_taken: float

@dataclass
class DbDiskResults:
    def __init__(self):
        self.start_time:str = ""
        self.end_time:str = ""
        self.elapsed_time:str = ""
        self.host_name:str = ""
        self.total_tables_dumped: int = 0
        self.total_rows_dumped: int = 0
        self.tables_cached:int = 0
        self.tables:list[TableInfo] = []

    
    def add_table(self, table_info: TableInfo):
        self.tables.append(table_info)
        self.tables_cached += 1