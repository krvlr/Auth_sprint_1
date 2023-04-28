import logging.config

from flask import Flask
from gevent import monkey

from core.config import settings, log_level
from core.logger import get_logging_config_dict

monkey.patch_all()

logging.config.dictConfig(get_logging_config_dict(log_level))

app = Flask(__name__)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=settings.debug_log_level,
    )
