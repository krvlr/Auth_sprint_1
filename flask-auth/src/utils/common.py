from typing import Type

from flask import abort, current_app, request
from pydantic import BaseModel, ValidationError


def get_body(request_model: Type[BaseModel]) -> dict:
    try:
        body = request_model.parse_obj(request.get_json())
        return body
    except ValidationError as err:
        current_app.logger.error(f"{err.__class__.__name__}: {err}")
        abort(422, description=err.errors())
