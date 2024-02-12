import unittest

from restq.http_cached_request import HttpCachedRequest
from restq.http_request import HttpRequest


class TestHttpRequest(unittest.TestCase):

    def setUp(self):
        self.http_request = HttpRequest('https://jsonplaceholder.typicode.com', None)
        self.http_cached_request = HttpCachedRequest('https://jsonplaceholder.typicode.com', None, 'C:\\temp\\restq')

    def test_http_request_request_get(self):
        response = self.http_request.request_get('posts?_limit=10')
        self.assertEqual(response.status_code, 200)

    def test_http_cached_request_get(self):
        response = self.http_cached_request.request_get('posts?_limit=10', 'posts')
        self.assertTrue(response is not None)

    def test_http_cached_request_get_should_result_from_cached(self):
        response = self.http_cached_request.request_get('invalid', 'posts')
        self.assertTrue(response is not None)
