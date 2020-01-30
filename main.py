from data_manager.data_manager import DataManager
from sense_hat import SenseHat
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

        signal.signal(signal.SIGSTOP, self.stop_prosses)
        signal.signal(signal.SIGTERM, self.stop_prosses)

        self.data_manager = DataManager(db_path, img_path)
        self.sense = SenseHat()

        self.start_time = datetime.now()
        self.stop_time = datetime.now() + timedelta(hours=2, minutes=58)
        self.data_manager.create_table() # TODO: if fasle (error) return

    def get_compass(self):
        for i in range(0,max_attempts):
            try:
                # Get axes with z ["z"], y ["y"], x ["x"]
                return self.sense.get_compass_raw()
            except Exception as e: 
                print(e)
            
        return None
    
    def get_img(self):
        for i in range(0,max_attempts):
            try:
                img = Image.capture_image()
                return img
            except Exception as e: 
                print(e)

        return None
    
    def save_to_db(self,img_raw,img_score,magnetic_field_raw):
        for i in range(0,max_attempts):
            try:
                self.data_manager.insert_data(img_raw,img_score,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
                break
            except Exception as e: 
                print(e)

        return None

    def remove_bad_score_img(self):
        row = self.data_manager.get_bad_score()
        id = self.data_manager.delete_img(row["id"], row["img_name"])
    
    def stop_prosses(self):
        self.stop = True

    def manager(self):
        if self.stop or self.stop_time <= datetime.now():
            self.data_manager.close()
            return
        

        compass_list = self.get_compass()
        img = self.get_img()

        self.save_to_db(img.id,img.score,compass_list)

        if self.data_manager.storage_available() == False: self.remove_bad_score_img()

        self.manager()

if __name__ == "__main__":
    main()