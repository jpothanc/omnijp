import os
import logging
from dotenv import load_dotenv

from src.common.caches.disk_cache_type import DiskFileType
from src.common.database.db_type import DbType
from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbrequest.db_request_builder import DbRequestBuilder
from tests.dbdisk.db_disk_request_test import CACHE_DIR
from src.ftps.ftps_request_builder import FtpsRequestBuilder


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('db_disk_test.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def db_disk_test():
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    logger = create_logger("db_disk_cache")
    try:
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_simple_cache")
            .set_connection_string(connection_string)
            .set_dump_all_tables(True)
            .set_list_tables_query("select table_name from information_schema.tables where table_schema = 'public'")
            # .set_table_list(["equities", "student"])
            # .set_can_zip(True)
            .set_dump_query("select * from equities")
            .set_rows_per_file(10)
        )).execute()
        print(result.to_json())
    except Exception as e:
        logger.exception("An error occurred:", e)
        pass
    finally:
        logger.info("Done")

def db_request_test():
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    logger = create_logger("db_request")
    try:
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(connection_string)
            .set_table_list(["equities", "student"])
            .set_query("select * from equities")
        )).execute()
        print(result.to_json())
        
        for table in result.tables:
            print(f"\nTable: {table.name}")
            print("Header:")
            print(table.header)
            print("Data:")
            for row in table.data:
                print(row)
        
    except Exception as e:
        logger.exception("An error occurred:", e)
        pass
    finally:
        logger.info("Done")



def ftps_pkcs_test():
    FtpsRequestBuilder.create(lambda x: (
        x.set_server("ftps://localhost")
        .set_port(990)
        .set_username("test")
        .set_cert_file("C:/temp/certificates/ftps/ftps.crt")
        .set_private_key_file("C:/temp/certificates/ftps/ftps.key")
        .set_local_path("C:/temp/ftps")
        .set_remote_path("/home/test")
    )).send()

if __name__ == "__main__":
    load_dotenv()
    # Set up logging in the application
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
         # ftps_pkcs_test()
          db_disk_test()
          db_request_test()
    except Exception as e:


        print(e)


