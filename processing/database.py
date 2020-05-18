import os
import sqlite3
from sqlite3 import Error

class DataBase:
    line = 0

    def __init__(self, db_path):
        super().__init__()

        try:
            self.conn = sqlite3.connect(os.path.abspath(db_path))
        except Error as e:
            raise SyntaxError(e)

    def next(self):
        pass

    def get_data(self):
        pass

    