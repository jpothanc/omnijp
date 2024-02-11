from urllib.parse import urljoin

import requests


class HttpRequest:
    def __init__(self, url, headers):
        self.base_url = url
        self.headers = headers

    def __str__(self):
        return f'{self.method} {self.base_url}'

    def request_get(self, url):
        full_url = urljoin(self.base_url, url)
        return requests.get(full_url, headers=self.headers or None)
