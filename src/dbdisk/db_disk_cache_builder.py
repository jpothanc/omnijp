from src.common.base_builder import BaseBuilder
from src.dbdisk.db_request_executer import DbDiskRequestExecutor
from src.dbdisk.models.db_disk_request import DbDiskRequest
from src.dbdisk.types import DbType, DiskFileType


class DbDiskCacheBuilder(BaseBuilder):
    def __init__(self):
        self.db_disk_request = DbDiskRequest()
        self.logger = None

    @classmethod
    def create(cls, setup):
        builder = cls()
        print("create")
        setup(builder)
        return builder
    
    def set_logger(self, logger):
        self.logger = logger
        return self

    def set_db_type(self, db_type: DbType):
        self.db_disk_request.db_type = db_type
        return self

    def set_disk_file_type(self, disk_file_type: DiskFileType):
        self.db_disk_request.disk_file_type = disk_file_type
        return self

    def set_cache_path(self, path):
        self.db_disk_request.cache_path = path
        return self

    def set_cache_name(self, name):
        self.db_disk_request.cache_name = name
        return self

    def set_connection_string(self, connection_string):
        self.db_disk_request.connection_string = connection_string
        return self

    def set_can_zip(self, can_zip):
        self.db_disk_request.can_zip = can_zip
        return self

    def set_rows_per_file(self, rows_per_file):
        self.db_disk_request.rows_per_file = rows_per_file
        return self
    def set_dump_all_tables(self,dump_all_tables ):
        self.db_disk_request.dump_all_tables = dump_all_tables
        return self

    def set_list_tables_query(self, list_tables_query):
        self.db_disk_request.list_tables_query = list_tables_query
        return self
    def set_table_list(self,table_list):
        self.db_disk_request.table_list = table_list
        return self
    
    def build(self):
        if  self.logger is None:
            self._create_default_console_logger()
        return self

    def execute(self, query):
        # self.db_disk_request.dump()
        self.build()
        self.db_disk_request.dump()
        with DbDiskRequestExecutor(self.db_disk_request, self.logger) as executor:
            return executor.execute(query)
