from dbdisk.caches.db_disk_cache_csv import DbDiskCacheCsv
from dbdisk.types import DiskFileType


class DbDiskFactory:
    @staticmethod
    def create_db_disk(file_type, cache_dir, cache_name, can_zip=False, rows_per_file=1000000):
        match file_type:
            case DiskFileType.CSV:
                return DbDiskCacheCsv(cache_dir, cache_name,can_zip, rows_per_file)
            case DiskFileType.JSON:
                raise NotImplementedError
            case DiskFileType.XML:
                raise NotImplementedError
            case _:
                return None

