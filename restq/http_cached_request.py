from restq.http_request import HttpRequest
from restq.disk_cache import DiskCache


class HttpCachedRequest(HttpRequest):
    def __init__(self, url, headers, cache_dir):
        super().__init__(url, headers)
        self.cache = DiskCache(cache_dir)

    def request_get(self, url, cache_name):
        result = super().request_get(url)
        if result.status_code == 200:
            self.cache.save(result.content, cache_name)
            return result.content
        return self.cache.load(cache_name)
