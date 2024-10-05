import os
import tempfile
from dataclasses import dataclass

from src.common.constants import  DB_REQUEST_RESULT_FILE
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
        output_file = self.output_file if self.output_file else os.path.join(tempfile.gettempdir(), DB_REQUEST_RESULT_FILE)
        return output_file
