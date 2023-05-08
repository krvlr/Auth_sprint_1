from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import get_jti, get_jwt, get_jwt_identity, jwt_required
from models.account import AuthUserDataResponse, SigninRequest, SignupRequest
from models.common import BaseResponse
from services.account import get_auth_service
from utils.common import get_body, set_jwt_in_cookie
from utils.exceptions import (
    AccountRefreshException,
    AccountSigninException,
    AccountSignupException,
)

account_bp = Blueprint("auth", __name__)
auth_service = get_auth_service()


@account_bp.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        body = get_body(SignupRequest)
        auth_service.signup(
            login=body.login,
            email=body.email,
            password=body.password,
        )

        response = jsonify(BaseResponse().dict())
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
        auth_data = AuthUserDataResponse(
            **auth_service.signin(
                login=body.login,
                password=body.password,
            )
        )

        response = jsonify(BaseResponse().dict())

        set_jwt_in_cookie(
            response=response,
            access_token=auth_data.access_token,
            refresh_token=auth_data.refresh_token,
        )

        return response, HTTPStatus.OK
    except AccountSigninException as error:
        response = jsonify(
            BaseResponse(success=False, error=error.error_message).dict()
        )
        return response, HTTPStatus.UNAUTHORIZED


@account_bp.route("/api/v1/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    refresh_jti = get_jwt()["jti"]

    try:
        auth_data = AuthUserDataResponse(
            **auth_service.refresh(
                user_id=current_user["id"],
                device_info=current_user["device_info"],
                refresh_jti=refresh_jti,
            )
        )

        response = jsonify(BaseResponse().dict())

        set_jwt_in_cookie(
            response=response,
            access_token=auth_data.access_token,
            refresh_token=auth_data.refresh_token,
        )

        return response, HTTPStatus.OK
    except AccountRefreshException as error:
        response = jsonify(
            BaseResponse(success=False, error=error.error_message).dict()
        )
        return response, HTTPStatus.BAD_REQUEST


# TODO: шаблон для ручeк /password/change, /signout, /signout/all, /history
#  с проверкой access_token (Only non-refresh tokens are allowed)
@account_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), HTTPStatus.OK
