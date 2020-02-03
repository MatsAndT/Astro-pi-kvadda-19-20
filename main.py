from data_manager.data_manager import DataManager
from datetime import datetime, timedelta
from sense_hat import SenseHat
from image import image
from logging import handlers
import signal
import os
import logging

max_attempts = 3
img_path = "./data/imgs/"
db_path = r"./data/database.sqlite"

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


class main():
    stop = False

    def __init__(self):
        logger.info('main init')
        super().__init__()

        signal.signal(signal.SIGSTOP, self.stop_prosses)
        signal.signal(signal.SIGTERM, self.stop_prosses)

        self.data_manager = DataManager(db_path, img_path)
        self.sense = SenseHat()

        self.start_time = datetime.utcnow()
        self.stop_time = datetime.utcnow() + timedelta(hours=2, minutes=58)
        self.data_manager.create_table()  # TODO: if false (error) return

        logger.debug('function main init end')

    def get_compass(self):
        logger.debug('function get_compass start')
        for i in range(0, max_attempts):
            try:
                # Get axes with z ["z"], y ["y"], x ["x"]
                logger.info('Returned compass info')
                return self.sense.get_compass_raw()
            except Exception as e:
                logger.critical('Could not get compass data: {}' /
                                .format(e))
                print(e)

        logger.debug('function __init__ end')
        return None

    def get_img(self):
        logger.debug('function get_img start')
        for i in range(0, max_attempts):
            try:
                logger.info('Captured image')
                img = Image.capture_image()
                return img
            except Exception as e:
                logger.critical('Could not get image: {}'.format(e))
                print(e)

        logger.debuge('function get_img end')
        return None

    def save_to_db(self, img_raw, img_score, magnetic_field_raw):
        logger.debug('function save_to_db start')
        for i in range(0, max_attempts):
            try:
                logger.debug('Saving to db')
                self.data_manager.insert_data(
                    img_raw, img_score, magnetic_field_raw[0], magnetic_field_raw[1], magnetic_field_raw[2])
                break
            except Exception as e:
                logger.critical('Could not save to database: {}'.format(e))
                print(e)

        logger.debug('function save_to_db end')
        return None

    def remove_bad_score_img(self):
        logger.debug('function remove_bad_score start')
        for i in range(0, max_attempts):
            try:
                bad_row = self.data_manager.get_bad_score()
                self.data_manager.delete_img(bad_row["img_name"])
                self.data_manager.delete_row(bad_row["id"])

            except Exception as e:
                logger.critical
                print(e)

        logger.debug('function remove_bad_score start')
        return None

    def stop_prosses(self):
        logger.info('function stop_prosess start')
        self.stop = True

    def manager(self):
        logger.info('function manager start')
        if self.stop or self.stop_time <= datetime.utcnow():
            self.data_manager.close()
            return

        compass_list = self.get_compass()
        img = self.get_img()

        self.save_to_db(img.id, img.score, compass_list)

        if self.data_manager.storage_available() == False:
            self.remove_bad_score_img()

        logger.debug('function manager end')
        self.manager()


if __name__ == "__main__":
    main()
