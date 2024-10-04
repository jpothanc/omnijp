import logging
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
    def execute(self, query)->DbResult:
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_request.db_type, self.db_request.connection_string)
        try:
           
            if self.db_request.table_list:
                self.logger.info(f"start dumping selected tables {self.db_request.table_list}")
                return self.dump_tables(db_service, self.db_request.table_list)
            else:
                self.logger.info(f"dumping query: {query}")
                results = DbResult()
                results.set_start_time()
                header, data = db_service.execute(query)
                table_result = TableResult(name="query", row_count=len(data), header=header, data=data)
                results.add_table(table_result)
                results.set_end_time()
                return results
        except Exception as e:
            raise Exception("Error querying db", e)
           



        