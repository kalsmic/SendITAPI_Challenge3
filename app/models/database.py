# app/models/database.py

import psycopg2
import psycopg2.extras as PG_EXTRAS
from config import app_config


class Database:


    def __init__(self):
        try:

            DATABASE_URL = "postgres://postgres:postgres@localhost:5432/sendit"
            self.conn = psycopg2.connect(DATABASE_URL)
            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=PG_EXTRAS.RealDictCursor)
        except (Exception, psycopg2.Error) as e:
            print(e)




    def create_tables(self):
        """Creates tables in the database"""
        # tuple contains queries for setting up tables in the database
        sql_queries = (
            """CREATE TABLE IF NOT EXISTS users ( userId serial PRIMARY  KEY,
                username VARCHAR(25),
                firstName varchar(25),
                lastName varchar(25),
                password varchar(255),
                email varchar (150));""",
            """CREATE TABLE IF NOT EXISTS parcels
            (
                order_id serial,
                item varchar(150),
                pick_up_location varchar(150),
                pick_up_date varchar(25),
                destination varchar(150),
                delivered_on varchar(25),
                status varchar(10),
                owner_id INTEGER,

                FOREIGN KEY (owner_id) REFERENCES users (userId) ON DELETE CASCADE ON UPDATE CASCADE
            );"""
        )
        for query in sql_queries:
            self.cur.execute(query)

    def empty_tables(self):
        sql_queries = ('Truncate users', 'Truncate parcels')
        for query in sql_queries:
            self.cur.execute(query)

