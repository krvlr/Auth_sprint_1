import json
from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "endpoint, data, expected_answer",
    [
        (
            "/signup",
            {
                "login": "kiras",
                "email": "kiras@me.com",
                "password": "12345678",
            },
            {"status": HTTPStatus.CREATED, "success": True},
        ),
    ],
)
async def test_registration(
    # postgre_engine,
    make_post_request,
    endpoint: str,
    data: dict,
    expected_answer: dict,
):
    response = await make_post_request(endpoint=endpoint, data=data)
    assert response.status == expected_answer["status"]
    assert response.body.get("success") == expected_answer["success"]
