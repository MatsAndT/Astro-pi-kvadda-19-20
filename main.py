import logging
import os
import signal
import atexit
from datetime import datetime, timedelta
from logging import handlers
from traceback import format_exc

try:
    from sense_hat import SenseHat
except ImportError: # Not on pi
    pass

from data_manager.data_manager import DataManager
from image import image

max_attempts = 3
abs_path = os.path.abspath(__file__)
img_path = abs_path + "/data/imgs/"
db_path = abs_path + "/data/database.sqlite"

image.path = img_path

filename = "log.log"

# if the logging is imported the root will be file name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# How the logs are going to look
formatter = logging.Formatter(
    '%(levelname)s:%(asctime)s:%(name)s:%(funcName)s:%(message)s')

# Creates a new log file every time it runs
should_roll_over = os.path.isfile(filename)
handler = logging.handlers.RotatingFileHandler(
    filename, mode='w', backupCount=10)
if should_roll_over:  # log already exists, roll over!
    handler.doRollover()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


class main:
    stop = False
    cycle = 0

    def __init__(self):
        logger.info('main init')

        atexit.register(self.stop_prosses)
        signal.signal(signal.SIGTERM, self.stop_prosses)

        # Test if the data and imgs path exist
        if not os.path.exists(img_path):
            logger.info("Data path not exist, create folders")
            os.makedirs(img_path)

        self.data_manager = DataManager(db_path, img_path)

        try:
            self.sense = SenseHat()
        except (OSError, NameError): # On pi without hat, or not testing on pi
            self.sense = __import__('fake_sense').SenseHat()
            logger.warning('Running without sense-hat')

        self.start_time = datetime.utcnow()
        self.stop_time = datetime.utcnow() + timedelta(seconds=15)

        logger.info('Program will end on {}'.format(self.stop_time))

        self.data_manager.create_table()  # TODO: if false (error) return

        logger.debug('function main init end')

    def get_compass(self):
        logger.debug('function get_compass start')
        for i in range(0, max_attempts):
            try:
                # Get axes with z ["z"], y ["y"], x ["x"]
                logger.debug('Returned compass info')
                return self.sense.get_compass_raw()
            except Exception as e:
                logger.critical('Could not get compass data: {}'.format(format_exc()))

        logger.debug('function get_compass end')
        return None

    def get_img(self):
        logger.debug('function get_img start')
        for i in range(0, max_attempts):
            try:
                logger.info('Captured image')
                img = image.Image.capture_image()
                return img
            except Exception as e:
                logger.critical('Could not get image: {}'.format(format_exc()))

        logger.debug('function get_img end')
        return None

    def save_to_db(self, img_name, img_score, magnetic_field_raw):
        logger.debug('function save_to_db start')
        for i in range(0, max_attempts):
            try:
                logger.debug('Saving to db')
                self.data_manager.insert_data(
                    img_name, img_score, magnetic_field_raw)
                break
            except Exception as e:
                logger.critical('Could not save to database: {}'.format(format_exc()))

        logger.debug('function save_to_db end')
        return None

    def remove_bad_score_img(self):
        logger.debug('function remove_bad_score start')
        for i in range(0, max_attempts):
            try:
                bad_row = self.data_manager.get_bad_score()
                print(bad_row)
                print("bad id: "+str(bad_row[0]))
                print("bad name: "+str(bad_row[1]))
                self.data_manager.delete_img(bad_row[1])
                self.data_manager.delete_row(bad_row[0])

            except Exception as e:
                logger.critical('Could not remove image: {}'.format(format_exc()))
                print("error bad: "+format_exc())

        logger.debug('function remove_bad_score start')
        return None

    def stop_prosses(self):
        logger.info('function stop_prosess start')
        self.stop = True

    def manager(self):
        logger.info('function manager start')

        while not self.stop or self.stop_time >= datetime.utcnow():
            self.cycle += 1
            print("On cycle: "+str(self.cycle))
            logger.info("On cycle"+str(self.cycle))

            print("Getting compass")
            compass_list = self.get_compass()
            
            print("Getting img")
            img = self.get_img()

            print("Save to db")
            self.save_to_db(img.id, img.score, compass_list)

            self.data_manager.add_img_size(img.id)

            del compass_list, img

            if self.data_manager.storage_available() == True:
                print("Remove bad img")
                self.remove_bad_score_img()

        self.data_manager.close()
        logger.debug('function manager end')


if __name__ == "__main__":
    main().manager()
