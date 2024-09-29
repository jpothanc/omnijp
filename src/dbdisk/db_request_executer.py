import os
from concurrent.futures import ThreadPoolExecutor

from src.dbdisk.database.db_service_factory import DbServiceFactory
from src.dbdisk.db_disk_factory import DbDiskFactory


class DbDiskRequestExecutor:
    def __init__(self, db_disk_request):
        self.db_disk_request = db_disk_request

    def execute(self, query):
        """
        execute the query and dump the result to disk
        :param query:
        :return:
        """
        db_service = DbServiceFactory.create_db_service(self.db_disk_request.db_type, self.db_disk_request.connection_string)
        try:
            if self.db_disk_request.dump_all_tables:
                print("start dumping all tables")
                return self.dump_all_tables(db_service, self.db_disk_request.list_tables_query)
            elif self.db_disk_request.table_list:
                print("start dumping selected tables", self.db_disk_request.table_list)
                return self.dump_tables(db_service, self.db_disk_request.table_list)
            else:
                print("dumping query:", query)
                header, data = db_service.execute(query)
                return DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        except Exception as e:
            raise Exception("Error dumping data to disk", e)


    def dump_tables(self,db_service, table_list):
        """
        dump selected tables
        :param table_list:
        :param db_service:
        :return:
        """
        print("start dumping selected tables")
        max_workers = min(5, os.cpu_count() + 4)  # Adjust based on CPU count and workload
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return executor.map(lambda x: self.dump_table(x, db_service), table_list)

    def dump_all_tables(self,db_service, list_tables_query):
        """
        dump all tables
        possible to provide a custom query to get all tables or use the default query
        :param db_service:
        :param list_tables_query:
        :return:
        """
        table_query = list_tables_query if list_tables_query is not None else db_service.get_all_tables_query()
        if table_query is "" or table_query is None:
            raise Exception("Does not know how to query all tables. Pls provide the query.")
        print("get all tables from db:",table_query)
        header, data = db_service.execute(table_query)
        table_list = [x[0] for x in data]
        return self.dump_tables(db_service, table_list)


    def dump_table(self,table, db_service):
        """
        dump table to disk
        :param table:
        :param db_service:
        :return:
        """
        query = f"select * from {table}"
        print("dumping table:", query)
        header, data =   db_service.execute(query)
        self.db_disk_request.cache_name =table
        print("creating db disk cache for table:", table)
        result =  DbDiskFactory.create_db_disk(self.db_disk_request).save(header, data)
        return result