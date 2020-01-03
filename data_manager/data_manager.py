import sqlite3
from sqlite3 import Error
import datetime


class DataManager():
    db_name = ""
    conn = sqlite3.connect
    cursor = conn.cursor

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except Error as e:
            print(e)
    
        return conn
    
    def create_table(self, conn):
        """ create a table from the table varibal
        :param conn: Connection object
        :return:
        """
        # TODO add the parameter for what data
        table = """CREATE TABLE IF NOT EXISTS sensor (
            id integer PRIMARY KEY,
            time timestamp,
        )"""
        try:
            c = conn.cursor()
            c.execute(table)
        except Error as e:
            print(e)


    def insert_data(self, conn, data):
        """
        Create a new project into the sensor table
        :param conn: Connection object
        :param data: Data to be inserted
        :return: project id
        """
        # TODO add the parameter for what data
        sql = ''' INSERT INTO sensor(name,begin_date,end_date)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, data)
        return cur.lastrowid

