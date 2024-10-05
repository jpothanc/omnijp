
import os
import shutil
import tempfile
import unittest

from dotenv import load_dotenv

from src.common.caches.disk_cache_type import DiskFileType
from src.common.constants import DB_REQUEST_RESULT_FILE
from src.common.database.db_type import DbType
from src.dbrequest.db_request_builder import DbRequestBuilder

CACHE_DIR = r"C:\temp\diskResultsTest"
OUTPUT_FILE = r"C:\temp\diskResultsTest\disk_postgres.txt"

class TestDBResultsRequest(unittest.TestCase):
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
            shutil.rmtree(CACHE_DIR)

    def tearDown(self):
        pass

    def validate_result(self, result):
        self.assertTrue(result.total_rows > 0)
        self.assertTrue(result.total_tables > 0)
        self.assertTrue(result.host_name is not None)
        self.assertTrue(result.start_time is not None)
        self.assertTrue(result.end_time is not None)

    def test_db_results_single_query_request(self):
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(self.connection_string)
            .set_query("select * from equities")
            .set_output_file(OUTPUT_FILE)
        )).execute()
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        self.validate_result(result)

    def test_creation_output_file_if_not_explicitly_provided(self):
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(self.connection_string)
            .set_query("select * from equities")
        )).execute()

        output_file_exists = os.path.exists(os.path.join(tempfile.gettempdir(),DB_REQUEST_RESULT_FILE))
        self.assertEqual(output_file_exists, True)
        self.validate_result(result)
    def test_db_results_single_table_request_fails(self):
        with self.assertRaises(Exception) as context:
            DbRequestBuilder.create(lambda x: (
                x.set_db_type(DbType.POSTGRESQL)
                .set_connection_string(self.connection_string)
                .set_output_file(OUTPUT_FILE)
            )).execute()

        self.assertTrue(context.exception is not None)

    def test_db_results_multiple_query_request(self):
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(self.connection_string)
            .set_query_list(["select * from equities", "select * from student"])
            .set_output_file(OUTPUT_FILE)
        )).execute()
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        self.validate_result(result)
        self.assertTrue(result.total_tables, 2)

    def test_db_results_table_list_request(self):
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(self.connection_string)
            .set_table_list(["equities", "student"])
            .set_output_file(OUTPUT_FILE)
        )).execute()
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        self.validate_result(result)
        self.assertTrue(result.total_tables == 2)