import asyncio
import logging

from src.common.database.db_service_factory import DbServiceFactory
from src.common.helper import json_to_file
from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.db_disk_request import DbDiskRequest
from src.dbdisk.db_disk_result import DbDiskResult
from src.dbdisk.executors.db_disk_executor import DbDiskExecutor


class DbBulkDiskRequestExecutor(DbDiskExecutor):
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
            result = asyncio.run(self.dump_single_query(db_service))
            json_to_file(result.to_json(), self.db_disk_request.result_output_file)
        except Exception as e:
            raise Exception("Error dumping data to disk", e)
        return result

    async def dump_single_query(self, db_service) -> DbDiskResult:
        result = await asyncio.get_event_loop().run_in_executor(None, self._dump_single_query, db_service)
        return result

    def _dump_single_query(self, db_service) -> DbDiskResult:
        result_generator = db_service.execute_chunk(self.db_disk_request.query, self.db_disk_request.rows_per_file)
        header = next(result_generator)
        result = DbDiskResult()
        result.set_start_time()
        cache_name = self.db_disk_request.cache_name
        for i, rows in enumerate(result_generator, start=1):
            logging.info(f"dumping chunk {i}")
            db_request = self.db_disk_request
            db_request.cache_name = f"{cache_name}{i:02d}"
            DbDiskFactory.create_db_disk(db_request).save_bulk(header, rows)
            result.total_rows_dumped += len(rows)
            result.total_chunks_dumped += 1
            logging.info(f"total rows dumped: {result.total_rows_dumped}")
        result.set_start_time()
        return result
