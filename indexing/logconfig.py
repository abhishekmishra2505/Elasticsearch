import logging
from logging.handlers import RotatingFileHandler


def get_logger(loggername,filename,consoleHandlerrequired=False):
        logger = logging.getLogger(loggername)
        logger.setLevel(logging.DEBUG)
        if not len(logger.handlers):
            handler = RotatingFileHandler(filename, maxBytes=200000,backupCount=50)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            if consoleHandlerrequired:
                ch = logging.StreamHandler()
                ch.setFormatter(formatter)
                logger.addHandler(ch)
            logger.addHandler(handler)
        return logger
