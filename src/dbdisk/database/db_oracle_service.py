class DbOracleService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def connect(self, query: str):
        import cx_Oracle
        return cx_Oracle.connect(self.connection_string)
