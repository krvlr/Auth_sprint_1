from flask import abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError
from typing import Type, Any


def get_data_from_body(request_model: Type[BaseModel]) -> Any:
    try:
        return request_model.parse_obj(request.get_json())
    except ValidationError as err:
        current_app.logger.error(f"{err.__class__.__name__}: {err}")
        abort(422, description=err.errors())


def set_jwt_in_cookie(response: jsonify, access_token: str, refresh_token: str):
    response.set_cookie("access_token_cookie", value=access_token, httponly=True)
    response.set_cookie("refresh_token_cookie", value=refresh_token, httponly=True)
