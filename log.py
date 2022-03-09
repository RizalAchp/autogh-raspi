import logging
import logging.handlers as handlers
import time
from pathlib import Path

class DynopyException(IOError):
    """class For main exception"""

class DynopyPortErrorException(DynopyException):
    """class for port related exceptions"""

class DynopyStop(DynopyException):
    """class for port related exceptions"""

def path_log(path: str) -> Path:
    ASSETS_PATH = Path(__name__).parent / Path(".log_data")
    # Menentukan Lokasi Asset Template
    return ASSETS_PATH / Path(path)

def log_exception(d):
    logger.error(d, exc_info=True)

def log_info(d):
    logger.info(d)

def log_error(d):
    logger.error(d)

def tes():
    while True:
        time.sleep(1)
        logger.info("A Sample Log Statement")
        logger.error("An error log statement")

logger = logging.getLogger('Dynotest_App')
logger.setLevel(logging.INFO)

# Here we define our formatter
formatter = logging.Formatter(
    '%(asctime)s  |  %(name)s  |  %(levelname)s  |  %(message)s')

logHandler = handlers.TimedRotatingFileHandler(
    path_log('app.log'), when='H', interval=1, backupCount=10
)

logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

errorLogHandler = handlers.RotatingFileHandler(
    path_log('error.log'), maxBytes=5000, backupCount=0
)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)


if __name__ == "__main__":
    log_exception("tes tes")
    tes()
