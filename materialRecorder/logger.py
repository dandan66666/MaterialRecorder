from logging import getLogger, Formatter, handlers, INFO, DEBUG
import logging
import time

def create_logger(app):
    log_path = 'log/materialRecorder'+time.strftime('%Y-%m-%d', time.localtime(time.time()))+'.log'

    file_handler = handlers.RotatingFileHandler(filename=log_path, maxBytes=100*1024*1024, backupCount=10)

    file_formatter = Formatter(fmt='[%(asctime)s] %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
