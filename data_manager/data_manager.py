import sqlite3
from sqlite3 import Error
import datetime


class DataManager():
    db_name = r"./astropi.db" # Path to Sqlite3 DB
    conn = sqlite3.connect # Is set to db after create_connection is run

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(self.db_name)

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
        :return: True

        If the table is stored correctly then a True is retuned, if not a False is retuned
        """
        # TODO add the parameter for what data
        table = """CREATE TABLE IF NOT EXISTS sensor_data (
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
        Inserting data into sensor_data tabel
        :param conn: Connection object
        :param img: Image to be inserted
        :return: project id

        Id is auto set : last++
        Time is a timestamp : saved as timestamp
        Img is stored as a blob
        Magnetometrer x y z raw data in uT micro teslas : saved as real)

        If Error is threw then Noen is returned 
        """
        # TODO add the parameter for what data
        sql = ''' INSERT INTO sensor_data(time,img,magnetometer)
                VALUES(?,?,?) '''
        
        try:
            cur = conn.cursor()
            cur.execute(sql, (datetime.now(), img, magnetometer))
            return cur.lastrowid
        except Error as e:
            print(e)
            return None

