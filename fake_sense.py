'''
A module used to simulate a SenseHat object for when
testing on a Pi without the sense-hat attatched.
'''

class SenseHat:
    def __init__(self, *args, **kwargs):
        pass

    def get_compass_raw(self):
        return {"x": 0, "y": 0, "z": 0}
