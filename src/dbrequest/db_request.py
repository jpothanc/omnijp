from dataclasses import dataclass

from src.dbdisk.types import DbType


@dataclass
class DbRequest:
    db_type = DbType.NONE
    connection_string = None
    table_list:list = None
