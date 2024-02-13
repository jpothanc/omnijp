from dbdisk.database_ps_service import DatabasePostgresService
from dbdisk.database_service import DatabaseService
from dbdisk.db_disk_factory import DbDiskFactory
from dbdisk.file_type import DbFileType


class DbDiskRequest:
    def __init__(self, connection_string, cache_dir, cache_name, file_type=DbFileType.CSV):
        self.connection_string = connection_string
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.db_service = DatabaseService(connection_string)
        self.file_type = file_type

    def execute(self, query):
        header, data = DatabasePostgresService.execute_query(self.connection_string, query)
        return DbDiskFactory.create_db_disk(self.file_type, self.cache_dir, self.cache_name).save(header, data)
