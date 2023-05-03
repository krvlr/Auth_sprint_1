from gevent import monkey

monkey.patch_all()

import logging.config

from api.v1 import account
from core.config import flask_settings
from core.logger import LOGGER_CONFIG
from db import init_db
from flask import Flask

logging.config.dictConfig(LOGGER_CONFIG)

app = Flask(__name__)

init_db(app)

app.register_blueprint(account.account_bp)

if __name__ == "__main__":
    app.run(
        host=flask_settings.host,
        port=flask_settings.port,
        debug=flask_settings.debug,
    )
