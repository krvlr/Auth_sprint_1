from http import HTTPStatus

from flask import Blueprint, jsonify
from flask_jwt_extended import (
    current_user,
    get_jti,
    get_jwt,
    jwt_required,
)

from models.auth_models import (
    AuthResponse,
    PasswordChangeRequest,
    SigninRequest,
    SignoutRequest,
    SignupRequest,
    PaginatorRequest,
)
from models.common import BaseResponse
from services.auth_service import get_auth_service
from utils.common import get_data_from_body, set_jwt_in_cookie, get_data_from_params
from utils.exceptions import (
    AccountPasswordChangeException,
    AccountRefreshException,
    AccountSigninException,
    AccountSignoutAllException,
    AccountSignoutException,
    AccountSignupException,
    AccountHistoryException,
)
from utils.user_action import log_action

account_bp = Blueprint("auth", __name__)
auth_service = get_auth_service()


@account_bp.route("/api/v1/signup", methods=["POST"])
@log_action
def signup():
    try:
        body = get_data_from_body(SignupRequest)
        user_data = auth_service.signup(
            login=body.login,
            email=body.email,
            password=body.password,
        )

        return jsonify(BaseResponse(data=user_data).dict()), HTTPStatus.CREATED
    except AccountSignupException as ex:
        return (
            jsonify(BaseResponse(success=False, error=ex.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )


@account_bp.route("/api/v1/signin", methods=["POST"])
@log_action
def signin():
    try:
        body = get_data_from_body(SigninRequest)
        auth_data = AuthResponse(
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
@log_action
def refresh():
    try:
        refresh_jwt_info = get_jwt()
        auth_data = AuthResponse(
            **auth_service.refresh(
                user_id=refresh_jwt_info["sub"]["id"],
                device_info=refresh_jwt_info["sub"]["device_info"],
                refresh_jti=refresh_jwt_info["jti"],
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
@log_action
def password_change():
    try:
        body = get_data_from_body(PasswordChangeRequest)

        response = auth_service.password_change(
            user=current_user,
            access_jti=get_jwt()["jti"],
            old_password=body.old_password,
            new_password=body.new_password,
        )
        return (
            jsonify(BaseResponse(success=True, data=response).dict()),
            HTTPStatus.OK,
        )
    except AccountPasswordChangeException as ex:
        return (
            jsonify(BaseResponse(success=False, error=ex.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )


@account_bp.route("/api/v1/signout", methods=["POST"])
@jwt_required()
@log_action
def signout():
    try:
        body = get_data_from_body(SignoutRequest)
        auth_service.signout(
            user_id=current_user.id,
            refresh_jti=get_jti(body.refresh_token),
            access_jti=get_jwt()["jti"],
        )

        return jsonify(BaseResponse().dict()), HTTPStatus.OK
    except AccountSignoutException as error:
        return (
            jsonify(BaseResponse(success=False, error=error.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )


@account_bp.route("/api/v1/signout/all", methods=["POST"])
@jwt_required()
@log_action
def signout_all():
    try:
        auth_service.signout_all(user_id=current_user.id, access_jti=get_jwt()["jti"])

        return jsonify(BaseResponse().dict()), HTTPStatus.OK
    except AccountSignoutAllException as error:
        return (
            jsonify(BaseResponse(success=False, error=error.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )


@account_bp.route("/api/v1/history", methods=["GET"])
@jwt_required()
def history():
    try:
        paginator = get_data_from_params(PaginatorRequest)
        history = auth_service.history(
            user_id=current_user.id,
            access_jti=get_jwt()["jti"],
            page_size=paginator.page_size,
            page_num=paginator.page_num,
        )

        return jsonify(BaseResponse(data=history).dict()), HTTPStatus.OK
    except AccountHistoryException as error:
        return (
            jsonify(BaseResponse(success=False, error=error.error_message).dict()),
            HTTPStatus.BAD_REQUEST,
        )
