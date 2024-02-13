from dbdisk.db_disk_cache_csv import DbDiskCacheCsv
from dbdisk.file_type import DbFileType


class DbDiskFactory:
    @staticmethod
    def create_db_disk(file_type, cache_dir, cache_name):
        match file_type:
            case DbFileType.CSV:
                return DbDiskCacheCsv(cache_dir, cache_name)
            case DbFileType.JSON:
                raise NotImplementedError
            case DbFileType.XML:
                raise NotImplementedError
            case _:
                return None

