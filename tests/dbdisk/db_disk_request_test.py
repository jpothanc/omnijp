import unittest

from dbdisk.db_disk_request import DbDiskRequest


class TestDbDiskRequest(unittest.TestCase):

    def setUp(self):
        pass

    def test_db_disk_request(self):
        connection_string = 'postgresql://jpothanc:Z2UXaMsCO3HV@ep-white-forest-89963536.ap-southeast-1.aws.neon.tech/datastore'
        result = DbDiskRequest(connection_string, 'c:\\temp', 'Users').execute('select * from Users where retired != 1')
        self.assertEqual(result, True)

    # def test_db_disk_request_will_fail(self):
    #     connection_string = 'postgresql://jpothan1c:Z2UXaMsCO3HV@ep-white-forest-89963536.ap-southeast-1.aws.neon.tech/datastore'
    #     result = DbDiskRequest(connection_string, 'c:\\temp', 'Users').execute('select * from Users where retired != 1')
    #     self.assertEqual(result, False)
