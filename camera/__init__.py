from camera import Camera

camera = Camera()

def __getattr__(attr):
    return getattr(camera, attr)

def __setattr__(attr, value):
    return setattr(camera, attr, value)