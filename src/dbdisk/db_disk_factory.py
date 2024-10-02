

from src.dbdisk.caches.db_disk_cache_csv import DbDiskCacheCsv
from src.dbdisk.types import DiskFileType


class DbDiskFactory:
    @staticmethod
    def create_db_disk(db_disk_request, logger):
        if db_disk_request.disk_file_type == DiskFileType.CSV:
            return DbDiskCacheCsv(db_disk_request.cache_path, db_disk_request.cache_name, db_disk_request.can_zip, db_disk_request.rows_per_file, logger)
        elif db_disk_request.disk_file_type == DiskFileType.JSON:
            raise NotImplementedError
        elif db_disk_request.disk_file_type == DiskFileType.XML:
            raise NotImplementedError
        else:
            return None