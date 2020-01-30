from sense_hat import SenseHat

class MagneticField():
    def __init__(self, *, sensehat=None):
        # Init the SenseHat class
        self.sense = SenseHat() if sensehat is None else sensehat

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