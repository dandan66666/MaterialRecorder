from flask import Flask
import os
from materialRecorder import db, record, config, logger

app = Flask(__name__, instance_relative_config=True)

db.init_app(app)

app.register_blueprint(record.mod)

if __name__ == '__main__':
    # load the instance config, if it exists, when not testing
    app.config.from_object(config.dev)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    logger.create_logger(app)

    # app.register_blueprint(record.mod)

    app.run(debug=True)
    # app.run()

