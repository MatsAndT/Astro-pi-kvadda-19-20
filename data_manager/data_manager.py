import logging
import os
import sqlite3
from datetime import datetime
from sqlite3 import Error
from traceback import format_exc
from time import sleep

# if the logging is imported the root will be file name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DataManager(object):
    total_image_data_size = 0

    def __init__(self, db_path, img_path):
        logger.info('Class DataManager init')

        super().__init__()
        self.db_name = db_path
        self.img_path = img_path

        try:
            self.conn = sqlite3.connect(os.path.abspath(self.db_name))

        except Error as e:
            logger.critical('Cannot connect to db: {}'.format(format_exc()))

        logger.debug('Class __init__ end')

    def create_table(self):
        """ create a table from the table varibal
        :return: True

        If the table is stored correctly then a True is retuned, if not a False is retuned
        """
        logger.debug('Function create_table start')

        table = """CREATE TABLE IF NOT EXISTS sensor_data (
            id integer PRIMARY KEY,
            time timestamp NOT NULL,
            img_name INTEGER,
            img_score INTEGER,
            magnetometer_z REAL,
            magnetometer_y REAL,
            magnetometer_x REAL
        );"""

        try:
            c = self.conn.cursor()

            # Create table
            c.execute(table)

            self.conn.commit()

            logger.info('Created a table')

            return True
        except Exception as e:
            table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='spwords'"
            if self.conn.execute(table_exists).fetchone() and isinstance(e, sqlite3.OperationalError):
                # sqlite3 docs say ProgrammingError is raised when table exists, although OperationalError was raised when testing.
                logger.warning('Table already exists: {}'.format(format_exc()))
                return True

            logger.critical('Could not create a table: {}'.format(format_exc()))
            return False

        logger.debug('Function create_table end')

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

        If Error is threw then None is returned 
        """
        logger.debug('Function insert_data start')

        sql = ''' INSERT INTO sensor_data(time,img_name,img_score,magnetometer_z,magnetometer_y,magnetometer_x)
                VALUES(?,?,?,?,?,?) '''

        try:
            cur = self.conn.cursor()

            # Insert a row of data
            cur.execute(sql, (datetime.now(), img_name, img_score,
                              magnetometer["z"], magnetometer["y"], magnetometer["x"]))

            self.conn.commit()

            logger.info('Inserted a row of data: id {}'.format(cur.lastrowid))

            return cur.lastrowid
        except Error as e:
            logger.critical('Could not insert data: {}'.format(format_exc()))
            return None
        logger.debug('Function insert_table end')

    def get_bad_score(self):
        """
        Getting img with bad score
        :return: bad score row
        """
        logger.debug('Function get_bad_score start')

        cur = self.conn.cursor()

        # Selecting worst score
        cur.execute(
            "SELECT id, img_name, img_score FROM sensor_data ORDER BY img_score ASC LIMIT 1")

        # Getting worst score
        rows = cur.fetchall()

        logger.debug('Function get_bad_score end')
        return rows[0]

    def delete_img(self, img_id):
        """
        Delete img with img_name
        :param img_id: Id of the img
        """
        logger.debug('Function delete_img start')

        logger.info("Deleting img: "+str(img_id))
        print("Deleting img: "+self.img_path+str(img_id)+".jpg")
        os.remove(self.img_path+str(img_id)+".jpg")

        logger.debug('Function delete_img end')

    def delete_row(self, id):
        """
        Delete row with id
        :param id: id of row
        """
        logger.debug('Function delete_row start')

        cur = self.conn.cursor()

        logger.info("Deleting row with id: "+str(id))
        print("Deleting row with id: "+str(id))
        cur.execute("DELETE FROM sensor_data WHERE id=?", (id,))

        self.conn.commit()

        logger.debug('Function delete_row end')

    def storage_available(self):
        """
        Se if the size of db is less then max_size
        :return: False (less) or True (bigger)
        """
        logger.debug('Function storage_available start')

        #max_size = 2.9*10**9
        # 0.1 GB test size
        max_size = 0.1*10**9

        if self.total_image_data_size >= max_size:
            logger.info("Storage available")
            print("Storage available")
            return False
        else:
            logger.info("Storage not available")
            print("Storage not available")
            return True

        logger.debug('Function storage_available end')

    def add_img_size(self, id):
        """
        Add the disk size off the image to total_image_data_size
        :param id
        """

        try:
            img_size = os.path.getsize("{}{}.jpg".format(self.img_path, id))
            print("img_size: {}".format(img_size))
        except FileNotFoundError as e:
            logger.warning('Could not find image file: {}'.format(e))

            try:
                # Sleeps two seconds if the OS is late
                sleep(2)

                img_size = os.path.getsize("{}{}.jpg".format(self.img_path, id))
            except FileNotFoundError as e:
                logger.warning('Could not find image attempt two file: {}'.format(e))

                img_size = 0
        finally:
            self.total_image_data_size += img_size
            print("total imge data: {}".format(self.total_image_data_size))

    def remove_img_size(self, id):
        """
        Remove the disk size off the image to total_image_data_size
        :param id
        """

        try:
            img_size = os.path.getsize("{}{}.jpg".format(self.img_path, id))
            print("img_size: {}".format(img_size))
        except FileNotFoundError as e:
            logger.warning('Could not find image file: {}'.format(e))

            try:
                # Sleeps two seconds if the OS is late
                sleep(2)

                img_size = os.path.getsize("{}{}.jpg".format(self.img_path, id))
            except FileNotFoundError as e:
                logger.warning('Could not find image attempt two file: {}'.format(e))

                img_size = 0
        finally:
            self.total_image_data_size -= img_size
            print("new total imge data: {}".format(self.total_image_data_size))

    def close(self):
        """
        Close the connection to the db
        :return True

        Just be sure any changes have been committed or they will be lost.

        If connection is not close then False is returned
        """
        logger.debug('Function close start')

        try:
            self.conn.commit()

            # Close the connection
            self.conn.close()
            logger.info("DB conn closed")
            return True
        except Error as e:
            logger.error('Could not close itself: {}'.format(e))
            return False

        logger.debug('Function close end')
