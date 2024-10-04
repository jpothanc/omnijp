from src.common.caches.disk_cache_csv import DiskCacheCsv
from src.common.caches.disk_cache_type import DiskFileType


class DbDiskFactory:
    @staticmethod
    def create_db_disk(db_disk_request):
        if db_disk_request.disk_file_type == DiskFileType.CSV:
            return DiskCacheCsv(db_disk_request.cache_path, db_disk_request.cache_name, db_disk_request.can_zip,
                                db_disk_request.rows_per_file)
        elif db_disk_request.disk_file_type == DiskFileType.JSON:
            raise NotImplementedError
        elif db_disk_request.disk_file_type == DiskFileType.XML:
            raise NotImplementedError
        else:
            return None
