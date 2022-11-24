import logging

logger = logging.getLogger('Telebot')


def configure_logging():

    # bot_handler = logging.FileHandler(filename='bot.log', mode='a')
    bot_handler = logging.StreamHandler()
    bot_formatter = logging.Formatter(
        fmt='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    bot_handler.setFormatter(bot_formatter)
    logger.addHandler(bot_handler)

    logger.setLevel(logging.DEBUG)
