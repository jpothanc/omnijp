from src.dbdisk.database.db_service import DbService
from src.dbdisk.database.db_service_factory import DbServiceFactory
from src.dbdisk.db_disk_factory import DbDiskFactory


class DbDiskRequest:
    def __init__(self, connection_string, db_type, cache_dir, cache_name, disk_file_type, can_zip, rows_per_file):
        self.connection_string = connection_string
        self.db_type = db_type
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.disk_file_type = disk_file_type
        self.can_zip = can_zip
        self.rows_per_file = rows_per_file

    def execute(self, query):
        db_service = DbServiceFactory.create_db_service(self.db_type, self.connection_string)
        header, data = db_service.execute(query)
        print(data)
        return DbDiskFactory.create_db_disk(self.disk_file_type, self.cache_dir, self.cache_name, self.can_zip,
                                            self.rows_per_file).save(header, data)
