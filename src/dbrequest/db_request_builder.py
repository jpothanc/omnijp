from src.common.database.db_type import DbType
from src.dbrequest.db_request import DbRequest
from src.dbrequest.db_request_executor import DbRequestExecutor
from src.dbrequest.db_results import DbResult


class DbRequestBuilder:
    def __init__(self):
        self.db_request = DbRequest()

    @classmethod
    def create(cls, setup):
        builder = cls()
        setup(builder)
        return builder
    
    def set_db_type(self, db_type: DbType):
        self.db_request.db_type = db_type
        return self
    def set_connection_string(self, connection_string):
        self.db_request.connection_string = connection_string
        return self
    def set_table_list(self, table_list):
        self.db_request.table_list = table_list
        return self
    def set_query(self, query):
        self.db_request.query = query
        return self
    def execute(self)->DbResult:
        with DbRequestExecutor(self.db_request) as executor:
            return executor.execute()

    

