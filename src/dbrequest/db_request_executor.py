import concurrent
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import time

from src.common.database.db_service_factory import DbServiceFactory
from src.dbrequest.db_request import DbRequest
from src.dbrequest.db_results import TableResult, DbResult


class DbRequestExecutor:
    def __init__(self, db_request: DbRequest):
        self.db_request = db_request
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def execute(self)->DbResult:
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_request.db_type, self.db_request.connection_string)
        try:
           
            if self.db_request.table_list:
                self.logger.info(f"start dumping selected tables {self.db_request.table_list}")
                return self.query_selected_tables(db_service, self.db_request.table_list)
            else:
                self.logger.info(f"dumping query: {self.db_request.query}")
                result = DbResult()
                result.set_start_time()
                header, data = db_service.execute(self.db_request.query)
                table_result = TableResult(name="query", row_count=len(data), header=header, data=data)
                result.add_table(table_result)
                result.set_end_time()
                return result
        except Exception as e:
            raise Exception("Error querying db", e)

    def query_selected_tables(self, db_service, table_list):
        """
        dump selected tables
        :param table_list:
        :param db_service:
        :return:
        """
        max_workers = min(5, os.cpu_count() + 4)  # Adjust based on CPU count and workload
        results = DbResult()
        results.set_start_time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dump_table_tasks = {executor.submit(self.query_table, table, db_service): table for table in table_list}

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(dump_table_tasks):
                table = dump_table_tasks[future]
                try:
                    table_info = future.result()
                    results.add_table(table_info)
                except Exception as exc:
                    self.logger.error(f"Table {table} generated an exception: {exc}")

        results.set_end_time()
        return results


    def query_table(self, table, db_service):
        """
        dump table to disk
        :param table:
        :param db_service:
        :return:
        """
        start_time = time.time()
        self.logger.info(f"dumping table: {table}")
        header, data = db_service.execute(self.db_request.query)
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)  # Round to 3 decimal places
        result = TableResult(name=table, row_count=len(data), header=header, data=data, time_taken=str(elapsed_time) + " ms")
        return result



        