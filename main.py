import os

from dotenv import load_dotenv

from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbdisk.types import DbType, DiskFileType
from tests.dbdisk.db_disk_request_test import CACHE_DIR

if __name__ == "__main__":
    load_dotenv()
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")

    try:
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_simple_cache")
            .set_connection_string(connection_string)
            .set_dump_all_tables(True)
            .set_list_tables_query("select table_name from information_schema.tables where table_schema = 'public'")
            .set_table_list(["equities", "student"])
        )).execute("select * from equities")
        print(result)
    except Exception as e:
        print(e)
    finally:
        print("Done")
