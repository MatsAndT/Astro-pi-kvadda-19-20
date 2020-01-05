from sense_hat import SenseHat

class MagneticField():
    def __init__(self):
        self.sense = SenseHat()

    def getCompass(self):
        compass = self.sense.get_compass_raw()

        return [compass['z'], compass['y'], compass['x']]