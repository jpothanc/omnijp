from dataclasses import dataclass

from src.common.database.db_type import DbType


@dataclass
class DbRequest:
    db_type = DbType.NONE
    connection_string = None
    table_list: list = None
    query = None
