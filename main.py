import os
import logging
from dotenv import load_dotenv

from src.common.caches.disk_cache_csv import DiskCacheCsv
from src.common.caches.disk_cache_type import DiskFileType
from src.common.database.db_service_factory import DbServiceFactory
from src.common.database.db_type import DbType
from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbrequest.db_request_builder import DbRequestBuilder
from src.ftps.ftps_request_builder import FtpsRequestBuilder

CACHE_DIR = r"C:\temp\diskCache"
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
            .set_connection_string(connection_string)
            # .set_dump_all_tables(True)
            .set_list_tables_query("select table_name from information_schema.tables where table_schema = 'public'")
            .set_table_list(["equities", "student"])
            .set_can_zip(True)
            .set_cache_name("users_simple_cache")
            .set_query("select * from equities")
            .set_rows_per_file(10)
            .set_output_file("db_disk_postgres_all.txt")
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
            # .set_table_list(["equities", "student"])
            # .set_query("select * from equities")
            .set_query_list(["select count(*) from equities", "select count(*) from student"])
            .set_output_file(r"c:\temp\disk_postgres.txt")
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


def db_chunk_test():
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    logger = create_logger("db_chunk")
    try:
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_connection_string(connection_string)
            .set_query("select * from student")
            .set_can_zip(True)
            .set_cache_name("student")
            .set_rows_per_file(100)
            .set_output_file("db_disk_postgres_all.txt")
            .set_bulk(True)
        )).execute()
        print(result.to_json())
    except Exception as e:
        logger.exception("An error occurred:", e)
        pass
    finally:
        logger.info("Done")
def db_chunk_test_raw():
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    logger = create_logger("db_chunk")
    try:
        db_service = DbServiceFactory.create_db_service(DbType.POSTGRESQL, connection_string)
        result_generator = db_service.execute_chunk("SELECT * FROM student", chunk_size=10)

        header = next(result_generator)  # Get the header
        print("Header:", header)
        
        for i, chunk in enumerate(result_generator, start=1):
                disk_cache = DiskCacheCsv(CACHE_DIR, f"student{i:02d}", can_zip=False)
                disk_cache.save_bulk(header, chunk)
                i += 1
    except Exception as e:
        logger.exception("An error occurred:", e)
        pass
    finally:
        logger.info("Done")

if __name__ == "__main__":
    load_dotenv()
    # Set up logging in the application
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
           # ftps_pkcs_test()
           # db_disk_test()
           # db_request_test()
             db_chunk_test()
    except Exception as e:
        print(e)



