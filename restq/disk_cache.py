import os
import pickle
from datetime import timedelta, datetime
import now as now


class DiskCache:
    def __init__(self, cache_dir, expires=timedelta(days=5)):
        self.cache_dir = cache_dir
        self.expires = expires

    def save(self, result, cache_name):
        try:
            formatted_date = datetime.now().strftime("%d-%m-%Y")
            filename = f"restq_{cache_name}_{formatted_date}.json"
            path = os.path.join(self.cache_dir, filename)
            folder = os.path.dirname(path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(path, 'wb') as fp:
                pickle.dump(result, fp)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def load(self, cache_name):
        try:
            formatted_date = datetime.now().strftime("%d-%m-%Y")
            filename = f"restq_{cache_name}_{formatted_date}.json"
            path = os.path.join(self.cache_dir, filename)
            with open(path, 'rb') as fp:
                return pickle.load(fp)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None

    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires
