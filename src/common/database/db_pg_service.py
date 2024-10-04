from src.common.database.db_service import DbService


class DbPgService(DbService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def connect(self):
        import psycopg2
        return psycopg2.connect(self.connection_string)

    def get_all_tables_query(self):
        return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' and table_type = 'BASE TABLE'"