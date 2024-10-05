from dataclasses import dataclass

from src.common.database.db_type import DbType


@dataclass
class DbRequest:
    db_type = DbType.NONE
    connection_string = None
    table_list: list = None
    query_list: list = None
    query = None
    output_file = None

    @property
    def result_output_file(self):
        return self.output_file
