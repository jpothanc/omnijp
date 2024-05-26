# omnijp
 OmniJP is a Python library that provides tools for common tasks in software development. 
It now supports features for caching database results to disk and making HTTP requests with caching support.

## Features

- **Database Disk Cache**: OmniJP provides a way to cache database results to disk. This is useful for large datasets that you don't want to query every time. The data is saved in CSV format and can be optionally zipped.

- **HTTP Requests**: OmniJP includes a simple HTTP request class with caching support. This can be used to make GET requests and cache the results for future use.

## Installation

You can install OmniJP using pip:

```bash
pip install omnijp
```

## Usage

Here's an example of how to use the `DbDiskCache` class to cache database results:

```python
from dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from dbdisk.types import DbType, DiskFileType

CONNECTION_STRING = "your_connection_string"

result = DbDiskCacheBuilder.create(lambda x: (
    x.set_db_type(DbType.POSTGRESQL)
    # currenty only csv is supported
    .set_disk_file_type(DiskFileType.CSV)
    .set_cache_path(r"C:\temp\diskCache")
    .set_cache_name("users")
    .set_connection_string(CONNECTION_STRING)
    .set_rows_per_file(1000)
    .set_can_zip(True)
)).execute("select * from Users where retired != 1")
```

And here's an example of how to use the `HttpCachedRequest` class to make a GET request and cache the result:

```python
from omnijp import HttpCachedRequest

http_cached_request = HttpCachedRequest().set_base_url('https://jsonplaceholder.typicode.com').\
    set_cache('C:\\temp\\restq').build()

response = http_cached_request.request_get('posts?_limit=10', 'posts')
```

## Testing

The library includes unit tests that you can run to verify its functionality. You can run the tests using the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.