from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from camera.camera import  Camera

data_manager = DataManager()
magnetic_field = MagneticField()

class Main():
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.magnetic_field = MagneticField()
        self.camera = Camera()

        self.conn = data_manager.create_connection()
        self.data_manager.create_table(conn) # TODO: if fasle (error) return

    def getCompass(self):
        for i in range(0,max_attamts):
            try:
                return magnetic_field_raw = self.magnetic_field.get_compass()
                break:
            except e:
                print(e)
    
    def getImg(self)
        for i in range(0,max_attamts):
            try:
                return img_raw = self.camera.capture_image()
                break:
            except e:
                print(e)
    
    def saveToDB(self,conn,magnetic_field_raw,img_raw):
        for i in range(0,max_attamts):
            try:
                data_manager.insert_data(conn,img_raw,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
                break:
            except e:
                print(e)
