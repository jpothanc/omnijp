import psycopg2


class DatabasePostgresService:
    @staticmethod
    def execute_query(connection_string, query):
        try:
            connection = psycopg2.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute(query)

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)

        finally:
            header = [desc[0] for desc in cursor.description]
            return header, cursor.fetchall()
            if cursor:
                cursor.close()
            if connection:
                connection.close()
