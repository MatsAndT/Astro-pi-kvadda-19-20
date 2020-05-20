import os
import sqlite3
from sqlite3 import Error

class Data:
    line = 0

    def __init__(self, db_path):
        super().__init__()

        try:
            self.conn = sqlite3.connect(os.path.abspath(db_path))
        except Error as e:
            raise SyntaxError(e)

    def add_colum(self):
        '''
        Add three column to the databse
        town : string
        county : string
        cotwo : string, it is for the co2 from the sheet
        '''
        cur = self.conn.cursor()
        cur.execute('alter table sensor_data add column town string')
        cur.execute('alter table sensor_data add column country string')
        cur.execute('alter table sensor_data add column cotwo string')
        self.conn.commit()
    
    def update_place(self, id, town, country):
        sql = 'UPDATE sensor_data SET town = ?, country = ? WHERE id = ?'
        
        cur = self.conn.cursor()
        cur.execute(sql, (town,country,id))
        self.conn.commit()

    def next(self):
        """
        Returns the next row of data to be prossest
        """

        row = self.conn.cursor().fetchone()[self.line]
        self.line += 1
        return row

    def get_data(self):
        pass

    