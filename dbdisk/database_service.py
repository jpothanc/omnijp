from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DatabaseService:

    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.session = sessionmaker(bind=self.engine)

    def execute(self, query):
        with self.session() as s:
            return s.execute(text(query))
