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
### DbDiskCache

You need a quick way to cache database results to disk, then you can use the `DbDiskCache` class.

Here's an example of how to cache database results:

```python
from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.common.caches.disk_cache_type import DiskFileType
from src.common.database.db_type import DbType

    CONNECTION_STRING = "your_connection_string"
    try:
        result = DbDiskCacheBuilder.create(lambda x: (
            # supported db types are POSTGRESQL, SYBASE and ORACLE
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(CONNECTION_STRING)
            # currently only csv is supported
            .set_disk_file_type(DiskFileType.CSV)
            # set the path where the cache files will be saved
            .set_cache_path(r"C:\temp\diskCache")
            # set the name of the cache
            .set_cache_name("users")
            # set the query to get the data from the database
            .set_query("select * from equities")
            # optional parameters, set the number of rows per file and whether to zip the files
            .set_rows_per_file(1000)
            .set_can_zip(True)
        )).execute()
        print(result.to_json())
    except Exception as e:
        print(e)
    finally:
        print("Completed")
```
Here's an example of how to cache all database tables:
```python
    
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_connection_string(connection_string)
            .set_dump_all_tables(True)            
        )).execute()
        
        
        result = DbDiskCacheBuilder.create(lambda x: (
            x.set_db_type(DbType.ORACLE)
            .set_disk_file_type(DiskFileType.CSV)
            .set_cache_path(CACHE_DIR)
            .set_connection_string(connection_string)
            .set_dump_all_tables(True)
            # provide a custom query to get the list of tables
            .set_list_tables_query("SELECT table_name FROM user_tables")
        )).execute()

  
```
Here's an example of how to cache selected tables:

```python
    result = DbDiskCacheBuilder.create(lambda x: (
        x.set_db_type(DbType.POSTGRESQL)
        .set_disk_file_type(DiskFileType.CSV)
        .set_cache_path(CACHE_DIR)
        .set_connection_string(connection_string)
        .set_table_list(["equities", "student"])
    )).execute()
  
```
### DBRequest
You need a quick way to make a database request and get the results, then you can use the `DBRequest` class.
Here's an example of how to use the `DBRequest` class to make a database request:

```python
    connection_string = os.getenv("LOCAL_CONNECTION_STRING")
    try:
        result = DbRequestBuilder.create(lambda x: (
            x.set_db_type(DbType.POSTGRESQL)
            .set_connection_string(connection_string)
            .set_query("select * from equities")
            # dump selected tables
            # .set_table_list(["equities", "student"])
        )).execute()
        print(result.to_json())
        
        for table in result.tables:
            print(f"\nTable: {table.name}")
            print("Header:")
            print(table.header)
            print("Data:")
            for row in table.data:
                print(row)
        
    except Exception as e:
        print(e)
    finally:
        print("Completed")  
```




### HttpCachedRequest
And here's an example of how to use the `HttpCachedRequest` class to make a GET request and cache the result:

```python
from omnijp import HttpCachedRequest

http_cached_request = HttpCachedRequest().set_base_url('https://jsonplaceholder.typicode.com').\
    set_cache('C:\\temp\\restq').build()

response = http_cached_request.request_get('posts?_limit=10', 'posts')
```
### AsyncOpenAIBot
And here's an example of how to use the `AsyncOpenAIBot` 
To use the AsyncOpenAIBot class, you need to provide a valid OpenAI API key when creating an instance of the class. 
This key is used to authenticate your requests to the OpenAI API.  

Here's a basic example of how to use the AsyncOpenAIBot class:

```python
import os
from src.openai.openai_bot import OpenAIBot


def my_callback(response):
    print("Received response:", response)


def run_bot_async():
    import asyncio
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = AsyncOpenAIBot(openai_key)
    while True:
        user_input = input("Enter your question:").lower()
        if user_input == "exit":
            break
        asyncio.run(openai_bot.get_response_async(user_input, my_callback))


if __name__ == "__main__":
    try:
        run_bot_async()
    except Exception as e:
        print(e)
```
In this example, my_callback is a function that will be called with the response from the OpenAI API.

### Secure File Transfer using PKCS12
PKCS12 (Public Key Cryptography Standards #12) is a binary format for storing cryptographic objects like private keys, certificates, and certificate chains in a single encrypted file.
Key Features:
Encryption: Private keys and certificates can be encrypted with a password.
Interoperability: Supported by multiple platforms (Java, OpenSSL, browsers, etc.).
File Extensions: .p12 or .pfx.
Extract the certificate and key from the p12 file
```commandline
 openssl pkcs12 -in <certificate.p12> -clcerts -nokeys -out <certificate.pem> -passin pass:<password>
 openssl pkcs12 -in <certificate.p12> -nocerts -nodes  -out <key.pem> -passin pass:<password>   
```

### OpenAIBot
Synchronous version of the OpenAIBot class
```python
def run_bot():
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = OpenAIBot(openai_key)
    response = openai_bot.get_response("1+1?")
    print("OpenAI Response:", response)
```
```python
if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(e)
```

#### Error Handling
The OpenAIBot class also handles some exceptions that might occur during the interaction with the OpenAI API:  
**openai.RateLimitError**: This exception is raised when the rate limit of the API is exceeded. The method raises a new exception with a custom message in this case.  
**openai.AuthenticationError**: This exception is raised when the authentication with the API fails (for example, if the API key is incorrect). The method raises a new exception with a custom message in this case.  
**openai.OpenAIError**: This is a general exception for other errors that might occur during the interaction with the API. The method raises a new exception with a custom message in this case.  
You can catch these exceptions in your code and handle them as needed.

## Testing

The library includes unit tests that you can run to verify its functionality. You can run the tests using the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.