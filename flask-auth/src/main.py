from gevent import monkey

monkey.patch_all()

from db.models import User
from utils.exceptions import add_base_exceptions_handlers

import logging.config
from datetime import timedelta

from api.v1 import auth_handler
from core.config import flask_settings, jwt_settings
from core.logger import LOGGER_CONFIG
from db import init_db
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flasgger import Swagger, LazyString, LazyJSONEncoder
from config.swagger import template, swagger_config

logging.config.dictConfig(LOGGER_CONFIG)


def create_app():
    app = Flask(__name__)

    Swagger(app, template=template, config=swagger_config)

    app.config["JWT_COOKIE_SECURE"] = jwt_settings.cookie_secure
    app.config["JWT_TOKEN_LOCATION"] = jwt_settings.token_location.split(", ")
    app.config["JWT_SECRET_KEY"] = jwt_settings.secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=jwt_settings.access_token_expires)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=jwt_settings.refresh_token_expires)

    add_base_exceptions_handlers(app)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return User.query.filter_by(id=jwt_data["sub"]["id"]).one_or_none()

    init_db(app)

    return app


app = create_app()
app.register_blueprint(auth_handler.auth_bp)

if __name__ == "__main__":
    app.run(
        host=flask_settings.host,
        port=flask_settings.port,
        debug=flask_settings.debug,
    )
