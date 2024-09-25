import concurrent.futures

from src.dbdisk.db_disk_factory import DbDiskFactory
from src.dbdisk.database.db_service_factory import DbServiceFactory


class DbDiskRequestExecutor:
    def __init__(self, db_disk_request):
        self.db_disk_request = db_disk_request

    def execute(self, query):
        db_service = DbServiceFactory.create_db_service(self.db_disk_request.db_type, self.db_disk_request.connection_string)
        try:
            if self.db_disk_request.dump_all_tables:
                print("start dump all tables")
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.dump_all_tables, db_service)
                    return future.result()
            else:
                print("dumping query:", query)
                header, data = db_service.execute(query)
                return DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        except Exception as e:
            raise Exception("Error dumping data to disk", e)


    def dump_all_tables(self,db_service):
        table_query = self.db_disk_request.list_tables_query if self.db_disk_request.list_tables_query else db_service.get_all_tables_query()
        print("get all tables from db:",table_query)
        header, data = db_service.execute(table_query)
        for table in data:
            query = f"select * from {table[0]}"
            print("dumping table:", query)
            header, data = db_service.execute(query)
            self.db_disk_request.cache_name = table[0]
            print("creating db disk cache for table:", table[0])
            return DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)