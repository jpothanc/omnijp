from urllib.parse import urljoin
import requests
from retry import retry


class HttpRequest:
    def __init__(self, url, headers):
        self.base_url = url
        self.headers = headers
        # Define a retry session with custom retry settings

    def __str__(self):
        return f'{self.method} {self.base_url}'

    # Decorate your function with the @retry decorator
    @retry(delay=1, backoff=2, max_delay=4, tries=3)
    def request_get(self, url):
        full_url = urljoin(self.base_url, url)
        return requests.get(full_url, headers=self.headers or None)
