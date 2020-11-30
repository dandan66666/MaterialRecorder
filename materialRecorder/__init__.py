from flask import Flask
import os
from . import db
from . import record
from . import config
from . import logger

# app = Flask(__name__, instance_relative_config=True)
#
# # load the instance config, if it exists, when not testing
# app.config.from_object(config.dev)
#
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass
#
# db.init_app(app)
#
# logger.create_logger(app)
#
# app.register_blueprint(record.mod)

# app.run()


