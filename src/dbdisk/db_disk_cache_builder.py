from src.common.base_builder import BaseBuilder
from src.common.caches.disk_cache_type import DiskFileType
from src.common.database.db_type import DbType
from src.dbdisk.executors.db_disk_bulk_executor import DbBulkDiskRequestExecutor
from src.dbdisk.executors.db_disk_bulk_offset_executor import DbDiskBulkOffsetExecutor
from src.dbdisk.db_disk_request import DbDiskRequest
from src.dbdisk.executors.db_disk_request_executer import DbDiskRequestExecutor
from src.dbdisk.dbdisk_executor_type import DbDiskExecutor


class DbDiskCacheBuilder(BaseBuilder):
    def __init__(self):
        self.db_disk_request = DbDiskRequest()

    @classmethod
    def create(cls, setup):
        builder = cls()
        setup(builder)
        return builder

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

    def set_dump_all_tables(self, dump_all_tables):
        self.db_disk_request.dump_all_tables = dump_all_tables
        return self

    def set_list_tables_query(self, list_tables_query):
        self.db_disk_request.list_tables_query = list_tables_query
        return self

    def set_table_list(self, table_list):
        self.db_disk_request.table_list = table_list
        return self

    def set_query(self, dump_query):
        self.db_disk_request.query = dump_query
        return self

    def set_output_file(self, output_file):
        self.db_disk_request.output_file = output_file
        return self

    def set_executor_type(self, executor_type:DbDiskExecutor):
        self.db_disk_request.executor_type = executor_type
        return self

    def execute(self):
        self.db_disk_request.dump()

        if self.db_disk_request.executor_type == DbDiskExecutor.BULK_DEFAULT:
            with DbBulkDiskRequestExecutor(self.db_disk_request) as executor:
                return executor.execute()
        elif self.db_disk_request.executor_type == DbDiskExecutor.BULK_OFFSET:
            with DbDiskBulkOffsetExecutor(self.db_disk_request) as executor:
                return executor.execute()
        else:
            with DbDiskRequestExecutor(self.db_disk_request) as executor:
                return executor.execute()
