from src.common.database.db_oracle_service import DbOracleService
from src.common.database.db_pg_service import DbPgService
from src.common.database.db_service import DbService
from src.common.database.db_sybase_service import DbSybaseService
from src.common.database.db_type import DbType


class DbServiceFactory:
    @staticmethod
    def create_db_service(db_type: DbType, connection_string: str) -> DbService:
        if db_type == DbType.POSTGRESQL:
            return DbPgService(connection_string)
        elif db_type == DbType.SYBASE:
            return DbSybaseService(connection_string)
        elif db_type == DbType.ORACLE:
            return DbOracleService(connection_string)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
