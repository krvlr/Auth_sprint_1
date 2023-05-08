from http import HTTPStatus

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, current_user

from models.auth_models import (
    AuthUserDataResponse,
    SigninRequest,
    SignupRequest,
    PasswordChangeRequest,
)
from models.common import BaseResponse
from services.auth_service import get_auth_service
from utils.common import set_jwt_in_cookie, get_data_from_body
from utils.exceptions import (
    AccountRefreshException,
    AccountSigninException,
    AccountSignupException,
    AccountPasswordChangeException,
)

account_bp = Blueprint("auth", __name__)
auth_service = get_auth_service()


@account_bp.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        body = get_data_from_body(SignupRequest)
        auth_service.signup(
            login=body.login,
            email=body.email,
            password=body.password,
        )

        response = jsonify(BaseResponse().dict())
        return response, HTTPStatus.CREATED
    except AccountSignupException as ex:
        response = jsonify(BaseResponse(success=False, error=ex.error_message).dict())
        return response, HTTPStatus.BAD_REQUEST


@account_bp.route("/api/v1/signin", methods=["POST"])
def signin():
    try:
        body = get_data_from_body(SigninRequest)
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
    except AccountSigninException as ex:
        return (
            jsonify(BaseResponse(success=False, error=ex.error_message).dict()),
            HTTPStatus.UNAUTHORIZED,
        )


@account_bp.route("/api/v1/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    refresh_jti = get_jwt()["jti"]

    try:
        auth_data = AuthUserDataResponse(
            **auth_service.refresh(
                user_id=current_user.id,
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
    except AccountRefreshException as ex:
        return (
            jsonify(BaseResponse(success=False, error=ex.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )


@account_bp.route("/api/v1/password/change", methods=["POST"])
@jwt_required()
def password_change():
    access_jti = get_jwt()["jti"]

    try:
        body = get_data_from_body(PasswordChangeRequest)

        response = auth_service.password_change(
            user=current_user,
            access_jti=access_jti,
            old_password=body.old_password,
            new_password=body.new_password,
        )
    except AccountPasswordChangeException as ex:
        return (
            jsonify(BaseResponse(success=False, error=ex.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )

    return (
        jsonify(BaseResponse(success=True, data=response).dict()),
        HTTPStatus.OK,
    )


# TODO: шаблон для ручeк /signout, /signout/all, /history
#  с проверкой access_token (Only non-refresh tokens are allowed)
@account_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), HTTPStatus.OK
