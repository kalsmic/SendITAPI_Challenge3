# app/models/database.py

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        try:

            DATABASE_URL = "postgres://postgres:postgres@localhost:5432/sendit"
            self.conn = psycopg2.connect(DATABASE_URL)
            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.Error) as e:
            print(e)

    def create_tables(self):
        """Creates tables in the database"""
        # tuple contains queries for setting up tables in the database
        sql_queries = (
            """create table if not exists users(
            user_id serial primary key,
            username varchar(25),
            firstname varchar(25),
            lastname varchar(25),
            password varchar(255),
            email varchar(150),
            is_admin boolean default false
            );""",
            """create table if not exists parcels (
            parcel_id serial not null,   
            item varchar(150),
            pick_up_location varchar(150),
            pick_up_date varchar(25),
            destination varchar(150),
            delivered_on varchar(25),
            status varchar(10),
            owner_id integer ,
            FOREIGN KEY (owner_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE );"""
        )
        for query in sql_queries:
            self.cur.execute(query)

    def empty_tables(self):
        sql_queries = ('Truncate users', 'Truncate parcels')
        for query in sql_queries:
            self.cur.execute(query)

if __name__ == "__main__":
    db = Database()
    db.create_tables()