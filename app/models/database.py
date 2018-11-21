# app/models/database.py

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        try:

            DATABASE_URL = "postgres://postgres:postgres@localhost:5432/sendit_test"
            self.conn = psycopg2.connect(DATABASE_URL)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.Error) as e:
            print(e)

    def create_tables(self):
        """Creates tables in the database"""
        # tuple contains queries for setting up tables in the database
        self.cursor.execute(open("/home/andela/Desktop/SentITAPI_Challenge3/schema.sql", "r").read())

    def empty_tables(self):
        sql_queries = ('Truncate users', 'Truncate parcels')
        for query in sql_queries:
            self.cursor.execute(query)


if __name__ == "__main__":
    db = Database()
    db.create_tables()
