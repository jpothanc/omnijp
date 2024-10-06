import os
import shutil
from itertools import islice
from datetime import datetime

def split_into_subsets(data, n):
    """
    Split the data into n subsets.
    """
    subsets = []
    iterable = iter(data)
    subset = list(islice(iterable, n))
    while subset:
        subsets.append(subset)
        subset = list(islice(iterable, n))
    return subsets

def zip_directory(directory, zip_name, delete_after_zip=True):
    """
    Zip the directory.
    """
    shutil.make_archive(zip_name, 'zip', directory)
    if delete_after_zip:
        shutil.rmtree(directory)

def getcurrenttime():
    """
    Get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3]

def json_to_file(json_data, file_path):
    """
    Write the json data to a file.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(json_data)
def generate_query_id(query):
    """
    Generate a unique id for the query.
    """
    return hash(query) % ((1 << 31) - 1)