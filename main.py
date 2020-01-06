from data_manager.data_manager import DataManager
from magnetometer.magnetometer import MagneticField
from camera.camera import capture_image

data_manager = DataManager()
magnetic_field = MagneticField()

conn = data_manager.create_connection()
data_manager.create_table(conn) # TODO: if fasle (error) return

while True:
    frame = capture_image()
    magnetic_field_raw = magnetic_field.getCompass()

    data_manager.insert_data(conn,frame,magnetic_field_raw[0],magnetic_field_raw[1],magnetic_field_raw[2])
    