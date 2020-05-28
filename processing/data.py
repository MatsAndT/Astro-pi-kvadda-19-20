import os
import sqlite3
from sqlite3 import Error
import csv
import shutil


class Data:
    line = 0
    co2 = {}

    def __init__(self, db_path, csv_path, folder):
        super().__init__()

        self.img_folder = os.path.abspath(os.getcwd()+'/'+folder)
        print(f'img folder: {self.img_folder}')
        self.init_co2(csv_path)

        try:
            self.conn = sqlite3.connect(os.path.abspath(db_path))
        except Error as e:
            raise SyntaxError(e)

    def init_co2(self, path):
        ''' Sets up the co2 map, with data from the csv '''
        with open(path) as csvfile:
            readCSV = [x for x in csv.reader(csvfile, delimiter=',')]
            countrys = readCSV[0]
            co2s = readCSV[1]
            
            for i in range(len(countrys)):
                self.co2[countrys[i]] = co2s[i]

            ##print(self.co2)
    
    def get_co2(self, country):
        return self.co2.get(country)

    def add_column(self):
        '''
        Add five column to the databse
        name : string
        region : string
        county : string
        cotwo : string, it is for the co2 from the sheet
        lat : string
        lon : string
        '''
        cur = self.conn.cursor()
        cur.execute('alter table sensor_data add column name string')
        cur.execute('alter table sensor_data add column region string')
        cur.execute('alter table sensor_data add column country string')
        cur.execute('alter table sensor_data add column cotwo string')
        cur.execute('alter table sensor_data add column lat string')
        cur.execute('alter table sensor_data add column lon string')
        self.conn.commit()
    
    def add_data(self, _id, name, region, country, co2, lat, lon):
        ''' Adds new data from internett to database '''
        sql = 'UPDATE sensor_data SET name = ?, region = ?, country = ?, cotwo = ?, lat = ?, lon = ? WHERE id = ?'
        
        cur = self.conn.cursor()
        cur.execute(sql, (name, region, country, co2, lat, lon, _id))
        self.conn.commit()

    def next(self):
        ''' Returns the next row of data to be prossest '''
        row = self.conn.cursor().execute('select id, time, img_name from sensor_data').fetchall()[self.line]
        self.line += 1
        return row

    def change_img_folder(self, img_name, country):
        name_start = 'teamkvadda_data_imgs_'
        try:
            os.renames(self.img_folder+'/'+name_start+str(img_name)+'.jpg', self.img_folder+'/'+'imgs/'+country+'/'+name_start+str(img_name)+'.png')
            print(f'img new path: imgs/{country}/{str(img_name)}.png')
        except Exception as e:
            print(f'did not manage to move img: {str(img_name)} to {country}')
            print(e)


    def close_conn(self):
        self.conn.close()
