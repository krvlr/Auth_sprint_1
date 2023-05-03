from http import HTTPStatus

from flask import Blueprint
from models.account import SignupRq, UserDataRs
from models.common import BaseResponse
from services import account
from utils.common import get_rq_from_body
from utils.exceptions import AccountSignupException

account_bp = Blueprint("auth", __name__)


@account_bp.route("/api/v1/signup", methods=["POST"])
def signup():
    signup_rq: SignupRq = get_rq_from_body(SignupRq)

    try:
        user_data = account.signup(
            login=signup_rq.login,
            email=signup_rq.email,
            password=signup_rq.password,
        )
    except AccountSignupException as ex:
        return (
            BaseResponse(success=False, error=ex.error_message).dict()
        ), HTTPStatus.BAD_REQUEST
    return (
        BaseResponse(success=True, data=UserDataRs(**user_data)).dict(),
        HTTPStatus.OK,
    )
