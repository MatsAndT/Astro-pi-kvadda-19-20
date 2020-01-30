from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from image import image
from datetime import datetime, timedelta
import os, signal

max_attempts = 3
img_path = "./data/imgs/"
db_path = r"./data/database.sqlite"

image.path = img_path

class main():
    stop = False

    def __init__(self):
        super().__init__()

        signal.signal(signal.SIGSTOP, self.stopProsses())
        signal.signal(signal.SIGTERM, self.stopProsses())

        self.data_manager = DataManager(db_path, img_path)
        self.magnetic_field = MagneticField()

        self.start_time = datetime.now()
        self.stop_time = datetime.now() + timedelta(hours=2, minutes=58)
        self.data_manager.create_table() # TODO: if fasle (error) return

    def getCompass(self):
        for i in range(0,max_attempts):
            try:
                # Get axes with z ["z"], y ["y"], x ["x"]
                return self.sense.get_compass_raw()
            except Exception as e: 
                print(e)
            
        return None
    
    def getImg(self):
        for i in range(0,max_attempts):
            try:
                return self.camera.capture_image()
            except Exception as e: 
                print(e)

        return None
    
    def saveToDB(self,img_raw,img_score,magnetic_field_raw):
        for i in range(0,max_attempts):
            try:
                self.data_manager.insert_data(img_raw,img_score,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
                break
            except Exception as e: 
                print(e)

        return None

    def manager(self):
        if self.stop: return
        if self.stop_time =< datetime.now(): return

        compass_list = self.getCompass()
        img = self.getImg()
        img_pros = Image(img)

        self.saveToDB(img,img_pros.score,compass_list)

        if self.data_manager.storage_available() == False: self.removeBadScoreImg()

        self.manager()

    def removeBadScoreImg(self):
        row = self.data_manager.get_bad_score()
        id = self.data_manager.delete_img(row["id"], row["img_name"])
    
    def stopProsses(self):
        self.stop = True

if __name__ == "__main__":
    main()