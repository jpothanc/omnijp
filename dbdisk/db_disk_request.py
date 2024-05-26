from dbdisk.database.database_pg_service import DatabasePgService
from dbdisk.database.database_service import DatabaseService
from dbdisk.db_disk_factory import DbDiskFactory
from dbdisk.types import DiskFileType


class DbDiskRequest:
    def __init__(self, connection_string, cache_dir, cache_name, file_type, can_zip, rows_per_file):
        self.connection_string = connection_string
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.db_service = DatabaseService(connection_string)
        self.file_type = file_type
        self.can_zip = can_zip
        self.rows_per_file = rows_per_file

    def execute(self, query):
        db_pg_service = DatabasePgService(self.connection_string)
        header, data = db_pg_service.execute(query)
        print(data)
        return DbDiskFactory.create_db_disk(self.file_type, self.cache_dir, self.cache_name, self.can_zip, self.rows_per_file).save(header, data)
