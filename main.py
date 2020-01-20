from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from camera.camera import Camera

max_attempts = 3

class Main():
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.magnetic_field = MagneticField()
        self.camera = Camera()

        self.conn = self.data_manager.create_connection()
        self.data_manager.create_table(self.conn) # TODO: if fasle (error) return

    def getCompass(self):
        for i in range(0,max_attempts):
            try:
                return self.magnetic_field.get_compass()
            except Exception as e: print(e)
    
    def getImg(self):
        for i in range(0,max_attempts):
            try:
                return self.camera.capture_image()
            except Exception as e: print(e)

    def imgScore(self,img):
        # TODO
        pass
    
    def saveToDB(self,img_raw,img_score,magnetic_field_raw):
        for i in range(0,max_attempts):
            try:
                self.data_manager.insert_data(self.conn,img_raw,img_score,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
                break
            except Exception as e: print(e)
