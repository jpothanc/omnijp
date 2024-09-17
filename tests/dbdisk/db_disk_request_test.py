import os
import shutil
import unittest

from dotenv import load_dotenv

from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbdisk.types import DbType, DiskFileType

CACHE_DIR = r"C:\temp\diskCache"
class TestDbDiskRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.connection_string = os.getenv("NEO_CONNECTION_STRING")
        print(f"Connection string: {cls.connection_string}")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        shutil.rmtree(CACHE_DIR)
        print(f"Deleted cache directory: {CACHE_DIR}")
    def tearDown(self):
        pass
    def test_db_disk_request(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_simple_cache")
            .set_connection_string(self.connection_string)
        )).execute("select * from Users where retired != 1")

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_simple_cache_1.csv"))
        self.assertEqual(cache_file_exists, True)
        self.assertEqual(result, True)

    def test_db_disk_request_with_split(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_split_cache")
            .set_connection_string(self.connection_string)
            .set_rows_per_file(2)
        )).execute("select * from Users where retired != 1")

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_split_cache_1.csv"))
        self.assertEqual(cache_file_exists, True)
        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_split_cache_2.csv"))
        self.assertEqual(cache_file_exists, True)

        self.assertEqual(result, True)

    def test_db_disk_request_with_split_and_zip(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(CACHE_DIR)
            .set_cache_name("users_zipped")
                            .set_connection_string(self.connection_string)
                            .set_rows_per_file(2)
                            .set_can_zip(True)
                            )).execute("select * from Users where retired != 1")

        cache_file_exists = os.path.exists(os.path.join(CACHE_DIR, "users_zipped.zip"))
        self.assertEqual(cache_file_exists, True)
        self.assertEqual(result, True)