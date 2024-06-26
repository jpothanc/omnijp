from src.dbdisk.caches.db_disk_cache_csv import DbDiskCacheCsv
from src.dbdisk.types import DiskFileType


class DbDiskFactory:
    @staticmethod
    def create_db_disk(disk_file_type, cache_dir, cache_name, can_zip=False, rows_per_file=1000000):
        match disk_file_type:
            case DiskFileType.CSV:
                return DbDiskCacheCsv(cache_dir, cache_name, can_zip, rows_per_file)
            case DiskFileType.JSON:
                raise NotImplementedError
            case DiskFileType.XML:
                raise NotImplementedError
            case _:
                return None
