from logging import getLogger, getLoggerClass, Formatter, handlers

def create_logger(app):

    file_handler = handlers.RotatingFileHandler(filename='log/materialRecorder.log', maxBytes=100*1024*1024, backupCount=10)

    file_formatter = Formatter(fmt='[%(asctime)s] %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel('INFO')

    app.logger.addHandler(file_handler)