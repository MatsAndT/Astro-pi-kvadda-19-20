from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from camera.camera import Camera
from datetime import datetime
import os

max_attempts = 3

class main():
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.magnetic_field = MagneticField()
        self.camera = Camera()

        self.start_time = datetime.now()
        self.conn = self.data_manager.create_connection()
        self.data_manager.create_table(self.conn) # TODO: if fasle (error) return

    def getCompass(self):
        for i in range(0,max_attempts):
            try:
                return self.magnetic_field.get_compass()
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

    def imgScore(self,img):
        # TODO
        return 100
    
    def saveToDB(self,img_raw,img_score,magnetic_field_raw):
        for i in range(0,max_attempts):
            try:
                self.data_manager.insert_data(self.conn,img_raw,img_score,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
                break
            except Exception as e: 
                print(e)

        return None

    def manager(self):
        compass_list = self.getCompass()
        img = self.getImg()
        img_score = self.imgScore(img)

        self.saveToDB(img,img_score,compass_list)

        if self.storageAvailable(): self.removeBadScore() else: pass

    def storageAvailable(self):
        max_size = 2.9*10**9

        try:
            b = os.path.getsize("./data_manager/astropi.sqlite")
        except FileNotFoundError as e:
            print(e)
        else:
            if b > max_size: return True 
            else: return False

    def removeBadScore(self):
        pass

if __name__ == "__main__":
    main()