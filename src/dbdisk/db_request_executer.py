import logging
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time

from src.dbdisk.database.db_service_factory import DbServiceFactory
from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.models.db_disk_request import DbDiskRequest
from src.dbdisk.models.db_disk_results import  DbDiskResults, TableInfo


class DbDiskRequestExecutor:
    def __init__(self, db_disk_request: DbDiskRequest):
        self.db_disk_request = db_disk_request
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, query):
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_disk_request.db_type, self.db_disk_request.connection_string)
        try:
            if self.db_disk_request.dump_all_tables:
                self.logger.info("start dumping all tables")
                return self.dump_all_tables(db_service, self.db_disk_request.list_tables_query)
            elif self.db_disk_request.table_list:
                self.logger.info(f"start dumping selected tables {self.db_disk_request.table_list}")
                return self.dump_tables(db_service, self.db_disk_request.table_list)
            else:
                self.logger.info(f"dumping query: {query}")
                results = DbDiskResults()
                results.set_start_time()
                header, data = db_service.execute(query)
                DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
                results.add_table(table_info=TableInfo(name="query", row_count=len(data)))
                results.set_end_time()
                return results
        except Exception as e:
            raise Exception("Error dumping data to disk", e)


    def dump_tables(self,db_service, table_list):
        """
        dump selected tables
        :param table_list:
        :param db_service:
        :return:
        """
        self.logger.info("start dumping selected tables")
        max_workers = min(5, os.cpu_count() + 4)  # Adjust based on CPU count and workload
        results = DbDiskResults()
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

    def dump_all_tables(self,db_service, list_tables_query):
        """
        dump all tables
        possible to provide a custom query to get all tables or use the default query
        :param db_service:
        :param list_tables_query:
        :return:
        """
        table_query = list_tables_query if list_tables_query is not None else db_service.get_all_tables_query()
        if table_query is "" or table_query is None:
            raise Exception("Does not know how to query all tables. Pls provide the query.")
        self.logger.info(f"get all tables from db: {table_query}")
        header, data = db_service.execute(table_query)
        table_list = [x[0] for x in data]
        return self.dump_tables(db_service, table_list)


    def dump_table(self,table, db_service):
        """
        dump table to disk
        :param table:
        :param db_service:
        :return:
        """
        star_time = time.time()
        query = f"select * from {table}"
        self.logger.info(f"dumping table: {query}")
        header, data =   db_service.execute(query)
        self.db_disk_request.cache_name =table
        self.logger.info(f"creating db disk cache for table: {table}")
        result =  DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        end_time = time.time()
        elapsed_time = round((end_time - star_time) * 1000, 3)  # Round to 3 decimal places
        table_info = TableInfo(name=table, row_count=len(data), time_taken=str(elapsed_time) + " ms")
        return table_info