from sense_hat import SenseHat

class MagneticField(SenseHat):
    def __init__(self, *args, **kwargs):
        # Init the SenseHat class
        sense = SenseHat()
        self.compass = sense.get_compass_raw()

    @property
    def magnetometer_z(self):
        # Return the comass rew compass data from z in uT (micro teslas)
        return self.compass['z']

    @property
    def magnetometer_y(self):
        # Return the comass rew compass data from y in uT (micro teslas)
        return self.compass['y']

    @property
    def magnetometer_x(self):
        # Return the comass rew compass data from x in uT (micro teslas)
        return self.compass['x']