import sqlite3, os
from sqlite3 import Error
from datetime import datetime


class DataManager(object):
    def __init__(self, db_path, img_path):
        super().__init__()
        self.db_name = db_path
        self.img_path = img_path

        try:
            self.conn = sqlite3.connect(self.db_name)
        except Error as e:
            print(e)
    
    def create_table(self):
        """ create a table from the table varibal
        :return: True

        If the table is stored correctly then a True is retuned, if not a False is retuned
        """
        
        table = """CREATE TABLE IF NOT EXISTS sensor_data (
            id integer PRIMARY KEY,
            time timestamp NOT NULL,
            img_name TEXT,
            img_score INTEGER,
            magnetometer_z REAL,
            magnetometer_y REAL,
            magnetometer_x REAL
        );"""

        try:
            # Getting cursor
            c = self.conn.cursor()

            # Create table
            c.execute(table)

            # Save (commit) the changes
            self.conn.commit()
            
            return True
        except Error as e:
            print(e)
            return False


    def insert_data(self, img_name, img_score, magnetometer):
        """
        Inserting data into sensor_data tabel
        :param img_name: Name of image
        :param img_score: Score of image
        :param magnetometer: Magnetometer data, z, y and x
        :return: project id

        Id is auto set : last++
        Time is a timestamp : saved as timestamp
        img_score i stored as a int
        Magnetometrer x y z raw data in uT micro teslas : saved as real)

        If Error is threw then Noen is returned 
        """
        
        sql = ''' INSERT INTO sensor_data(time,img_score,magnetometer_z,magnetometer_y,magnetometer_x)
                VALUES(?,?,?,?,?) '''
        
        try:
            # Getting cursor
            cur = self.conn.cursor()

            # Insert a row of data
            cur.execute(sql, (datetime.now(), img_name, img_score, magnetometer["z"], magnetometer["y"], magnetometer["x"]))

            # Save (commit) the changes
            self.conn.commit()

            return cur.lastrowid
        except Error as e:
            print(e)
            return None

    def get_bad_score(self):
        """
        Getting img with bad score
        :return: bad score row
        """

        # Getting cursor
        cur = self.conn.cursor()

        # Selecting worst score
        cur.execute("SELECT id, img_name, img_score FROM sensor_data ORDER BY img_score ASC LIMIT 1")

        # Getting worst score
        rows = cur.fetchall()

        return rows[0]

    def delete_img(self, id, img_name):
        """
        Delete img with img_name
        :param id: id of row
        :param img_name: Name of the img
        :return: Deleted id of row
        """

        # Getting cursor
        cur = self.conn.cursor()

        # Delets the row with id = id
        print("Deletes img from: "+str(id)+", img_name: "+str(img_name))
        ##cur.execute("DELETE FROM sensor_data WHERE id=?", (id))
        os.remove(self.img_path+"/"+img_name)
        print("File removed")

        # Save (commit) the changes
        self.conn.commit()

        return id

    def storage_available(self):
        """
        Se if the size of db is less then max_size
        :return: False (less) or True (bigger)
        """

        max_size = 2.9*10**9

        try:
            b = os.path.getsize(self.img_path+"../")
        except FileNotFoundError as e:
            print(e)
        else:
            if b > max_size: return False 
            else: return True

    def close(self):
        """
        Close the connection to the db
        :return True

        Just be sure any changes have been committed or they will be lost.

        If connection is not close then False is returned
        """

        try:
            # Save (commit) the changes
            self.conn.commit()

            # Close the connection
            self.conn.close()
            return True
        except Error as e:
            print(e)
            return False
