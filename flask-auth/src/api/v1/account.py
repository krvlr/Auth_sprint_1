from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import (
    get_jti,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)
from models.account import SigninRequest, SignupRequest
from models.common import BaseResponse
from services.account import AuthService
from utils.common import get_body
from utils.exceptions import AccountSigninException, AccountSignupException

account_bp = Blueprint("auth", __name__)


@account_bp.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        body = get_body(SignupRequest)
        user_data = AuthService.signup(
            login=body.login,
            email=body.email,
            password=body.password,
        )
        response = jsonify(BaseResponse(data=user_data.dict()).dict())
        return response, HTTPStatus.CREATED
    except AccountSignupException as error:
        response = jsonify(
            BaseResponse(success=False, error=error.error_message).dict()
        )
        return response, HTTPStatus.BAD_REQUEST


@account_bp.route("/api/v1/signin", methods=["POST"])
def signin():
    try:
        body = get_body(SigninRequest)
        auth_data = AuthService.signin(
            login=body.login,
            password=body.password,
        )

        response = jsonify(BaseResponse().dict())
        set_access_cookies(response, auth_data.access_token)
        set_refresh_cookies(response, auth_data.refresh_token)
        current_app.logger.info(f"jti = {get_jti(auth_data.refresh_token)}")
        return response, HTTPStatus.OK
    except AccountSigninException as error:
        response = jsonify(
            BaseResponse(success=False, error=error.error_message).dict()
        )
        return response, HTTPStatus.UNAUTHORIZED


# шаблон для примера ручки с проверкой access_token (Only non-refresh tokens are allowed)
@account_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), HTTPStatus.OK


# шаблон для примера ручки /refresh (Only refresh tokens are allowed)
@account_bp.route("/refresh_protected", methods=["GET"])
@jwt_required(refresh=True)
def refresh_protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), HTTPStatus.OK
