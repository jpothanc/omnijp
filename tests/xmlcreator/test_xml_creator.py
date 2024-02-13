import os.path
import unittest

from xmlcreator.xml_creator import XmlCreator


class TestXmlCreator(unittest.TestCase):

    def setUp(self):
        pass

    def test_xml_creator(self):
        XmlCreator.create_xml_file('c:\\temp', 'test.xml', name='John', age=30)
        file_path = os.path.join('c:\\temp', 'test.xml')
        self.assertEqual(os.path.exists(file_path), True)

    def test_xml_creator_will_fail(self):
        pass
