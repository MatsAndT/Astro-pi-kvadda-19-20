from sense_hat import SenseHat

class MagneticField():
    def __init__(self, *, sensehat=None):
        # Init the SenseHat class
        self.sense = SenseHat() if sensehat is None else sensehat

    def getCompass(self):
        # Getting the raw compass data
        compass = self.sense.get_compass_raw()

        # Return the comass rew compass data from z, y and x in uT (micro teslas)
        return [compass['z'], compass['y'], compass['x']]
