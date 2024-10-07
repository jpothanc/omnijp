import os
from dataclasses import dataclass

from src.common.caches.disk_cache_type import DiskFileType
from src.common.constants import DB_DISK_RESULT_FILE
from src.common.database.db_type import DbType
from src.dbdisk.dbdisk_executor_type import DbDiskExecutor

MAX_ROWS = 1000000


@dataclass
class DbDiskRequest:
    db_type: DbType = DbType.NONE
    disk_file_type: DiskFileType = DiskFileType.CSV
    cache_path: str = None
    cache_name: str = None
    connection_string: str = None
    db_type: DbType = None
    can_zip: bool = False
    rows_per_file: int = MAX_ROWS
    dump_all_tables: bool = False
    list_tables_query: str = None
    table_list: list = None
    query = None
    output_file = None
    executor_type:DbDiskExecutor = DbDiskExecutor.DEFAULT

    @property
    def result_output_file(self):
        output_file = self.output_file if self.output_file else DB_DISK_RESULT_FILE
        return os.path.join(self.cache_path, output_file)

    def dump(self):
        print("\nClass Members:")
        for name, value in vars(self).items():
            print(f"{name}: {value}")
