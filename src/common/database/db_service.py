import logging
from abc import abstractmethod

import psycopg2
import pymssql

from src.common.helper import generate_query_id


class DbService:

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def execute(self, query):
        connection = None
        cursor = None
        try:
            query_id = generate_query_id(query)
            self.logger.debug("start executing query: (%s) %s", query_id,query)
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            header = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
            self.logger.debug("end executing query: (%s) %s", query_id,query)
        except Exception as e:
            self.handle_error(e)
            result = None
            header = None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return header, result

    def execute_chunk(self, query, chunk_size):

        connection = None
        cursor = None
        try:
            query_id = generate_query_id(query)
            self.logger.debug("start executing query: (%s) %s", query_id, query)
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            header = [desc[0] for desc in cursor.description]
            yield header  # Yield the header first
            while True:
                rows = cursor.fetchmany(chunk_size)
                if not rows:
                    break
                yield rows
            self.logger.debug("end executing query: (%s) %s", query_id, query)
        except Exception as e:
            self.handle_error(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @abstractmethod
    def connect(self):
        pass

    @staticmethod
    def handle_error(error):
        error_messages = {
            psycopg2.Error: "Error connecting to PostgresSQL:",
            pymssql.Error: "Error connecting to Sybase:"
        }
        error_type = type(error)
        message = error_messages.get(error_type, "Unknown error")
        raise Exception(message, error)

    @abstractmethod
    def get_all_tables_query(self):
        pass
