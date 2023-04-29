from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    success: bool = True
    error: str | list | dict | None = None
    data: Any = None
