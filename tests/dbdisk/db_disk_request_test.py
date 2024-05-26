import unittest

from dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from dbdisk.types import DbType

CONNECTION_STRING = 'postgresql://jpothanc:Z2UXaMsCO3HV@ep-white-forest-89963536.ap-southeast-1.aws.neon.tech/datastore'
class TestDbDiskRequest(unittest.TestCase):

    def setUp(self):
        pass

    def test_db_disk_request(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(r"C:\temp\diskCache")
            .set_cache_name("users_simple_cache")
            .set_connection_string(CONNECTION_STRING)
        )).execute("select * from Users where retired != 1")

        self.assertEqual(result, True)

    def test_db_disk_request_with_split(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(r"C:\temp\diskCache")
            .set_cache_name("users_split_cache")
            .set_connection_string(CONNECTION_STRING)
            .set_rows_per_file(2)
        )).execute("select * from Users where retired != 1")

        self.assertEqual(result, True)

    def test_db_disk_request_with_split_and_zip(self):
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_cache_path(r"C:\temp\diskCache")
            .set_cache_name("users_zipped")
                            .set_connection_string(CONNECTION_STRING)
                            .set_rows_per_file(2)
                            .set_can_zip(True)
                            )).execute("select * from Users where retired != 1")

        self.assertEqual(result, True)