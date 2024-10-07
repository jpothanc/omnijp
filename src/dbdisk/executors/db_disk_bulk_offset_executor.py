import concurrent
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from src.common.database.db_service_factory import DbServiceFactory
from src.common.helper import json_to_file
from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.db_disk_request import DbDiskRequest
from src.dbdisk.db_disk_result import DbDiskResult, TableDumpResult
from src.dbdisk.executors.db_disk_executor import DbDiskExecutor

TABLE_NAME = "student"


class DbDiskBulkOffsetExecutor(DbDiskExecutor):
    def __init__(self, db_disk_request: DbDiskRequest):
        super().__init__(db_disk_request)

    def execute(self) -> DbDiskResult:
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_disk_request.db_type,
                                                        self.db_disk_request.connection_string)
        try:
            logging.info(f"starting bulk executor : {self.db_disk_request.query}")
            result = self.dump_table(db_service, TABLE_NAME)
            json_to_file(result.to_json(), self.db_disk_request.result_output_file)
        except Exception as e:
            raise Exception("Error dumping data to disk", e)
        return result

    def dump_table(self, db_service, table_name) -> DbDiskResult:
        """
        dump the table to disk
        :param db_service:
        :param table_name:
        :return:
        """

        total_rows = self._get_row_count(db_service, table_name)
        chunk_size = self.db_disk_request.rows_per_file

        # range(0, total_rows, CHUNK_SIZE) generates numbers starting from 0 up to total_rows (exclusive), incrementing by CHUNK_SIZE at each step.
        # This means it creates chunks of rows with size CHUNK_SIZE.
        chunk_starts = [(db_service, table_name, i, chunk_size, file_num)
                        for file_num, i in enumerate(range(0, total_rows, chunk_size), start=1)]

        max_workers = self._thread_workers
        result = DbDiskResult()
        result.set_start_time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dump_table_tasks = {executor.submit(self._dump_table, *chunk_start): chunk_start
                                for chunk_start in chunk_starts}

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(dump_table_tasks):
                table = dump_table_tasks[future]
                try:
                    table_info = future.result()
                    result.total_chunks_dumped += 1
                    result.add_table(table_info)
                except Exception as exc:
                    self.logger.error(f"Table {table} generated an exception: {exc}")

        result.set_end_time()
        return result

    def _dump_table(self, db_service, table_name, start_row, chunk_size, file_num) -> TableDumpResult:
        """
        dump a chunk of the table to disk
        :param db_service:
        :param table_name:
        :param start_row:
        :param chunk_size:
        :param file_num:
        :return:
        """
        start_time = time.time()
        query = f"SELECT * FROM {table_name} OFFSET {start_row} LIMIT {chunk_size};"
        logging.info(f"Dumping chunk {file_num} of {query}")
        header, data = db_service.execute(query)
        cache_name = f"{self.db_disk_request.cache_name}{file_num:02d}"
        DbDiskFactory.create_db_disk(self.db_disk_request).save_bulk(header, data, cache_name)
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)  # Round to 3 decimal places
        result = TableDumpResult(name=TABLE_NAME, row_count=len(data), time_taken=str(elapsed_time) + " ms")
        return result

    def _get_row_count(self, db_service, table_name):
        """
        get the row count of the table
        :param db_service:
        :param table_name:
        :return:
        """
        try:
            query = f"SELECT count(*) FROM {table_name};"
            _, data = db_service.execute(query)
            return data[0][0]
        except Exception as e:
            raise Exception(f"Error getting row count for table {table_name}", e)
