import logging
from typing import Type

from flask import abort, request
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def get_rq_from_body(request_model: Type[BaseModel]):
    try:
        body = request_model.parse_obj(request.get_json())
    except ValidationError as err:
        logger.error("{}: {}", err.__class__.__name__, err)
        error_message = err.errors()
        abort(422, description=error_message)
    else:
        return body
