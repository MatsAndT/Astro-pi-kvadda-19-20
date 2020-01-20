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
        