import logzero
from logzero import logger

# These log messages are sent to the console
logger.debug("hello")
logger.info("info")
logger.warning("warning")
logger.error("error")

# This is how you'd log an exception
try:
    raise Exception("this is a demo exception")
except Exception as e:
    logger.exception(e)

logzero.logfile("log.txt", formatter=None, mode="a", maxBytes=10000, 
backupCount=2, encoding=None, loglevel=None, disableStderrLogger=False)