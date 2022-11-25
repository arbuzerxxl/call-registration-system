import logging
from tornado import log

logger = logging.getLogger('UserAppealLog')


def configure_logging():

    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        fmt='%(levelname)s: [%(asctime)s]: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    logger.setLevel(logging.INFO)
