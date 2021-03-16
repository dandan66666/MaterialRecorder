from flask import Flask
import os
from materialRecorder import db, record, config, logger, api
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)

db.init_app(app)

app.register_blueprint(record.mod)
app.register_blueprint(api.mod)
logger.create_logger(app)


if __name__ == '__main__':
    # load the instance config, if it exists, when not testing
    app.config.from_object(config.dev)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # app.register_blueprint(record.mod)

    app.run(debug=True)
    # app.run()

