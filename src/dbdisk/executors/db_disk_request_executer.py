import asyncio
import concurrent.futures
import time
from concurrent.futures import ThreadPoolExecutor

from src.common.database.db_service_factory import DbServiceFactory
from src.common.helper import json_to_file
from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.db_disk_request import DbDiskRequest
from src.dbdisk.db_disk_result import DbDiskResult, TableDumpResult
from src.dbdisk.executors.db_disk_executor import DbDiskExecutor


class DbDiskRequestExecutor(DbDiskExecutor):
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
            if self.db_disk_request.dump_all_tables:
                self.logger.info("start dumping all tables")
                result = self.dump_all_tables(db_service, self.db_disk_request.list_tables_query)
                json_to_file(result.to_json(), self.db_disk_request.result_output_file)
                return result
            elif self.db_disk_request.table_list:
                self.logger.info(f"start dumping selected tables {self.db_disk_request.table_list}")
                result = self.dump_selected_tables(db_service, self.db_disk_request.table_list)
                json_to_file(result.to_json(), self.db_disk_request.result_output_file)
                return result
            else:
                self.logger.info(f"dumping query: {self.db_disk_request.query}")
                result = asyncio.run(self.dump_single_query(db_service))
                json_to_file(result.to_json(), self.db_disk_request.result_output_file)
                return result
        except Exception as e:
            raise Exception("Error dumping data to disk", e)

    async def dump_single_query(self, db_service) -> DbDiskResult:
        result = await asyncio.get_event_loop().run_in_executor(None, self._dump_single_query, db_service)
        return result

    def _dump_single_query(self, db_service) -> DbDiskResult:
        result = DbDiskResult()
        result.set_start_time()
        header, data = db_service.execute(self.db_disk_request.query)
        DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        result.add_table(table_info=TableDumpResult(name="query", row_count=len(data)))
        result.set_end_time()
        return result

    def dump_selected_tables(self, db_service, table_list) -> DbDiskResult:
        """
        dump selected tables
        :param table_list:
        :param db_service:
        :return:
        """
        max_workers = self._thread_workers
        results = DbDiskResult()
        results.set_start_time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dump_table_tasks = {executor.submit(self.dump_table, table, db_service): table for table in table_list}

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

    def dump_all_tables(self, db_service, list_tables_query) -> DbDiskResult:
        """
        dump all tables
        possible to provide a custom query to get all tables or use the default query
        :param db_service:
        :param list_tables_query:
        :return:
        """
        table_query = list_tables_query if list_tables_query is not None else db_service.get_all_tables_query()
        if table_query == "" or table_query is None:
            raise Exception("Does not know how to query all tables. Pls provide the query.")

        self.logger.info(f"Getting all tables from db: {table_query}")
        header, data = db_service.execute(table_query)
        table_list = [x[0] for x in data]
        return self.dump_selected_tables(db_service, table_list)

    def dump_table(self, table, db_service) -> TableDumpResult:
        """
        dump table to disk
        :param table:
        :param db_service:
        :return:
        """
        start_time = time.time()
        self.logger.info(f"dumping table: {table}")
        query = f"select * from {table}"
        header, data = db_service.execute(query)
        self.db_disk_request.cache_name = table
        self.logger.info(f"creating db disk cache for table: {table}")
        DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)  # Round to 3 decimal places
        result = TableDumpResult(name=table, row_count=len(data), time_taken=str(elapsed_time) + " ms")
        return result
