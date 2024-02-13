import os
import csv
from dbdisk.db_disk_cache import DbDiskCache


class DbDiskCacheCsv(DbDiskCache):
    def save(self, header, data):
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            file_path = os.path.join(self.cache_dir, f"{self.cache_name}.csv")
            with open(file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                for row in data:
                    csv_writer.writerow(row)
        except Exception as e:
            print(f"Error saving cache: {e}")
            return False
        print(f"Cache saved to {file_path}")
        return True
