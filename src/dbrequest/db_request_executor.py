import concurrent
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor

from src.common.database.db_service_factory import DbServiceFactory
from src.common.helper import json_to_file
from src.dbrequest.db_request import DbRequest
from src.dbrequest.db_result import TableResult, DbResult


class DbRequestExecutor:
    def __init__(self, db_request: DbRequest):
        self.db_request = db_request
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self) -> DbResult:
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_request.db_type, self.db_request.connection_string)
        try:

            if self.db_request.table_list:
                self.logger.info(f"start querying selected tables {self.db_request.table_list}")
                result = self.query_selected_tables(db_service, self.db_request.table_list)
                json_to_file(result.to_json(), self.db_request.result_output_file)
                return result
            elif self.db_request.query_list:
                self.logger.info(f"start querying selected queries {self.db_request.query_list}")
                result = self.query_list(db_service, self.db_request.query_list)
                json_to_file(result.to_json(), self.db_request.result_output_file)
                return result

            else:
                self.logger.info(f"start single query: {self.db_request.query}")
                result = DbResult()
                result.set_start_time()
                table_result = self.query_single(self.db_request.query, db_service)
                result.add_table(table_result)
                result.set_end_time()
                json_to_file(result.to_json(), self.db_request.result_output_file)
                return result
        except Exception as e:
            raise Exception("Error querying db", e)

    def query_selected_tables(self, db_service, table_list):
        """
        query selected tables
        :param table_list:
        :param db_service:
        :return:
        """
        max_workers = self._thread_workers
        results = DbResult()
        results.set_start_time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dump_table_tasks = {executor.submit(self.query_table, table, db_service): table for table in table_list}

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(dump_table_tasks):
                table = dump_table_tasks[future]
                try:
                    TableResult = future.result()
                    results.add_table(TableResult)
                except Exception as exc:
                    self.logger.error(f"Table {table} generated an exception: {exc}")

        results.set_end_time()
        return results

    def query_list(self, db_service, query_list) -> DbResult:
        """
        query selected tables
        :param query_list:
        :param db_service:
        :return DbResult:
        """
        max_workers = self._thread_workers
        results = DbResult()
        results.set_start_time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dump_table_tasks = {executor.submit(self.query_single, query, db_service): query for query in query_list}

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(dump_table_tasks):
                table = dump_table_tasks[future]
                try:
                    TableResult = future.result()
                    results.add_table(TableResult)
                except Exception as exc:
                    self.logger.error(f"Table {table} generated an exception: {exc}")

        results.set_end_time()
        return results

    def query_table(self, table, db_service) -> TableResult:
        """
        query table
        :param table:
        :param db_service:
        :return TableResult:
        """
        start_time = time.time()
        query = f"select * from {table}"
        self.logger.info(f"dumping table: {table}")
        header, data = db_service.execute(query)
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)  # Round to 3 decimal places
        result = TableResult(name=table, row_count=len(data), header=header, data=data,
                             time_taken=str(elapsed_time) + " ms")
        return result

    def query_single(self, query, db_service) -> TableResult:
        """
        query single
        :param query:
        :param db_service:
        :return:
        """
        start_time = time.time()
        header, data = db_service.execute(query)
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)  # Round to 3 decimal places
        result = TableResult(name=query, row_count=len(data), header=header, data=data,
                             time_taken=str(elapsed_time) + " ms")
        return result

    @property
    def _thread_workers(self):
        return min(5, os.cpu_count() + 4)

    def execute_chunk(self, query, db_service, chunk_size):
        """
        execute the query in chunks
        :param query:
        :param db_service:
        :param chunk_size:
        :return:
        """
        pass