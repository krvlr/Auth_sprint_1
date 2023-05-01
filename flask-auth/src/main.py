import logging.config

from flask import Flask
from gevent import monkey

from api.v1 import account
from core.config import settings, log_level
from core.logger import get_logging_config_dict
from db import init_db

monkey.patch_all()

logging.config.dictConfig(get_logging_config_dict(log_level))

app = Flask(__name__)

init_db(app)

app.register_blueprint(account.account_bp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=settings.debug_log_level,
    )
