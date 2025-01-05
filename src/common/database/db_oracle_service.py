from src.common.database.db_service import DbService


class DbOracleService(DbService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def connect(self):
        import cx_Oracle
        return cx_Oracle.connect(self.connection_string)
    def get_all_tables_query(self):
        #SELECT table_name FROM user_tables
        return ""