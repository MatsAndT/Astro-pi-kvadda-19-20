import os
import sqlite3
from sqlite3 import Error
import csv

class Data:
    line = 0
    co2 = {}

    def __init__(self, db_path, csv_path):
        super().__init__()

        self.init_co2(csv_path)

        try:
            self.conn = sqlite3.connect(os.path.abspath(db_path))
        except Error as e:
            raise SyntaxError(e)

    def init_co2(self, path):
        '''
        Sets up the co2 map, with data from the csv
        '''
        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            countrys = readCSV[0]
            co2s = readCSV[1]

            for i in range(countrys):
                self.co2[countrys[i]] = co2s[i]

            print(self.co2)
            

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

    