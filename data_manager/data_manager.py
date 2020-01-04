import sqlite3
from sqlite3 import Error
from datetime import datetime


class DataManager():
    db_name = r"./astropi.sqlite"
    conn = None # Is set to db after create_connection is run

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None

        If link was not made then None is returned
        """
        try:
            # Connecting to db
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
        # TODO: add the parameter for what data
        table = """CREATE TABLE IF NOT EXISTS sensor_data (
            id integer PRIMARY KEY,
            time timestamp NOT NULL,
            img blob,
            magnetometer real NOT NULL
        );"""

        try:
            # Getting cursor
            c = conn.cursor()

            # Create table
            c.execute(table)

            # Save (commit) the changes
            conn.commit()
            
            return True
        except Error as e:
            print(e)
            return False


    def insert_data(self, conn, img, magnetometer):
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
        # TODO: add the parameter for what data
        sql = ''' INSERT INTO sensor_data(time,img,magnetometer)
                VALUES(?,?,?) '''
        
        try:
            # Getting cursor
            cur = conn.cursor()

            # Insert a row of data
            cur.execute(sql, (datetime.now(), img, magnetometer))

            # Save (commit) the changes
            conn.commit()

            return cur.lastrowid
        except Error as e:
            print(e)
            return None
<<<<<<< HEAD

    def close(self, conn):
        """
        Close the connection to the db
        :param conn: Connection object
        :return True

        Just be sure any changes have been committed or they will be lost.

        If connection is not close then False is returned
        """

        try:
            # Save (commit) the changes
            conn.commit()

            # Close the connection
            conn.close()
            return True
        except Error as e:
            print(e)
            return False

=======
>>>>>>> 83204fe0e866501bde698707c1d9e82c929726d4
