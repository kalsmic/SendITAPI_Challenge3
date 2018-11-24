# app/models/database.py

from os import environ

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(environ.get('DATABASE_URL'))
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.Error) as e:
            print(e)


    def create_tables(self):
        """Creates tables in the database"""
        # tuple contains queries for setting up tables in the database
        self.cursor.execute(open("schema.sql", "r").read())

    def empty_tables(self):
        self.cursor.execute('DELETE FROM parcels')
        self.cursor.execute('DELETE FROM users WHERE user_id > 2')


if __name__ == "__main__":
    db = Database()
    db.create_tables()
