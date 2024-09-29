from src.dbdisk.database.db_service import DbService
from src.dbdisk.database.db_service_factory import DbServiceFactory
from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.types import DiskFileType, DbType

MAX_ROWS = 1000000
class DbDiskRequest:
    def __init__(self):
        self.db_type = DbType.NONE
        self.disk_file_type = DiskFileType.CSV
        self.cache_path = None
        self.cache_name = None
        self.connection_string = None
        self.db_type = None
        self.can_zip = False
        self.rows_per_file = MAX_ROWS
        self.dump_all_tables = False
        self.list_tables_query = None
        self.table_list = []
    def dump(self):
        print("\nClass Members:")
        for name, value in vars(self).items():
            print(f"{name}: {value}")



