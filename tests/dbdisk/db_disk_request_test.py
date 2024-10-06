import math
import os
import unittest

from dotenv import load_dotenv
from parameterized import parameterized

from src.common.caches.disk_cache_type import DiskFileType
from src.common.constants import DB_DISK_RESULT_FILE
from src.common.database.db_type import DbType
from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder

CACHE_DIR = r"C:\temp\diskCacheTest"
OUTPUT_FILE = r"db_disk_custom.txt"


class TestDbDiskRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.connection_string = os.getenv("LOCAL_CONNECTION_STRING")
        print(f"Connection string: {cls.connection_string}")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        if os.path.exists(CACHE_DIR):
            pass
            # shutil.rmtree(CACHE_DIR)

    def tearDown(self):
        pass

    def validate_result(self, result):
        self.assertTrue(result.total_rows_dumped > 0)
        self.assertTrue(result.total_tables_dumped > 0)
        self.assertTrue(result.host_name is not None)
        self.assertTrue(result.start_time is not None)
        self.assertTrue(result.end_time is not None)

    def test_db_disk_request(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_simple_cache")
            .set_connection_string(self.connection_string)
            .set_query("select * from equities")
            .set_output_file(OUTPUT_FILE)
        )).execute()

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_simple_cache.csv"))
        self.assertEqual(cache_file_exists, True)
        output_file_exists = os.path.exists(os.path.join(CACHE_DIR, OUTPUT_FILE))
        self.assertEqual(output_file_exists, True)
        self.validate_result(result)

    @parameterized.expand([
        ["student_cache", "select * from student", True, 10],
        ["equities_cache", "select * from equities", False,1000]
    ])
    def test_db_disk_request_bulk(self, cache_name, query, zip_file, rows_per_file):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_connection_string(self.connection_string)
            .set_cache_name(cache_name)
            .set_query(query)
            .set_rows_per_file(rows_per_file)
            .set_output_file(OUTPUT_FILE)
            .set_bulk(True)  
            .set_can_zip(zip_file)
        )).execute()

        cache_file_name = f"{cache_name}01.zip" if zip_file else f"{cache_name}01.csv"
        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, cache_file_name))

        print(f"Cache file exists: {cache_file_name}")
        self.assertEqual(cache_file_exists, True)
        output_file_exists = os.path.exists(os.path.join(CACHE_DIR, OUTPUT_FILE))
        self.assertEqual(output_file_exists, True)
        # total chunks created will be 
        count =   math.ceil(result.total_rows_dumped / rows_per_file)
        self.assertTrue(result.total_chunks_dumped,  count)


    def test_creation_output_file_if_not_explicitly_provided(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_simple_cache")
            .set_connection_string(self.connection_string)
            .set_query("select * from equities")
        )).execute()

        output_file_exists = os.path.exists(os.path.join(CACHE_DIR, DB_DISK_RESULT_FILE))
        self.assertEqual(output_file_exists, True)
        self.validate_result(result)

    def test_db_results_single_table_request_fails(self):
        with self.assertRaises(Exception) as context:
            DbDiskCacheBuilder.create(lambda x: (
                x.set_db_type(DbType.POSTGRESQL)
                .set_connection_string(self.connection_string)
                .set_output_file(OUTPUT_FILE)
            )).execute()

        self.assertTrue(context.exception is not None)

    def test_db_disk_request_dump_all_tables(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_dump_all_tables(True)
            .set_connection_string(self.connection_string)
            .set_output_file(OUTPUT_FILE)
        )).execute()

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "equities.csv"))
        self.assertEqual(cache_file_exists, True)
        output_file_exists = os.path.exists(os.path.join(CACHE_DIR, OUTPUT_FILE))
        self.assertEqual(output_file_exists, True)

        self.validate_result(result)

    def test_db_disk_request_dump_table_list(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_table_list(["equities", "student"])
            .set_connection_string(self.connection_string)
        )).execute()

        valid_cache_files = os.path.exists(os.path.join(CACHE_DIR, "equities.csv")) and os.path.exists(
            os.path.join(CACHE_DIR, "student.csv"))
        self.assertEqual(valid_cache_files, True)
        self.validate_result(result)
        self.assertEqual(result.total_tables_dumped, 2)

    def test_db_disk_request_with_split(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_split_cache")
            .set_connection_string(self.connection_string)
            .set_rows_per_file(2)
            .set_query("select * from equities")
        )).execute()

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_split_cache_1.csv")) and os.path.exists(
            os.path.join(CACHE_DIR, "users_split_cache_2.csv"))
        self.assertEqual(cache_file_exists, True)
        self.validate_result(result)

    def test_db_disk_request_with_split_and_zip(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_zipped")
            .set_connection_string(self.connection_string)
            .set_rows_per_file(2)
            .set_can_zip(True)
            .set_query("select * from equities")
        )).execute()

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_zipped.zip"))
        self.assertEqual(cache_file_exists, True)
        self.validate_result(result)
