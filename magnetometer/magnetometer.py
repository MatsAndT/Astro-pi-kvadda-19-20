from sense_hat import SenseHat

class MagneticField():
    def __init__(self, *, sensehat=None):
        # Init the SenseHat class
        self.sense = SenseHat() if sensehat is None else sensehat

    @property
    def magnetometer_z(self):
        # Return the comass rew compass data from z in uT (micro teslas)
        return self.compass['z']

        # Return the comass rew compass data from z, y and x in uT (micro teslas)
        return [compass['z'], compass['y'], compass['x']]
