from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from camera.camera import capture_image

data_manager = DataManager()
magnetic_field = MagneticField()

conn = data_manager.create_connection()
data_manager.create_table(conn) # TODO: if fasle (error) return
