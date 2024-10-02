import os
import logging
from dotenv import load_dotenv

from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbdisk.types import DbType, DiskFileType
from tests.dbdisk.db_disk_request_test import CACHE_DIR
from src.ftps.ftps_request_builder import FtpsRequestBuilder

def db_disk_test():
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Create a file handler
    file_handler = logging.FileHandler('db_disk_test.log')
    file_handler.setLevel(logging.INFO)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create a formatting for the logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
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
            # .set_logger(logger)  # Pass the logger here
        )).execute("select * from equities")
        print(result)
    except Exception as e:
        logger.exception("An error occurred:")
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
    try:
        # ftps_pkcs_test()
        db_disk_test()
    except Exception as e:

        print(e)


