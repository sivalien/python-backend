"""Подразумевается, что при запуске тестов локально запущено приложение.

Адрес: localhost:8000
"""
from __future__ import annotations

from http import HTTPStatus
from typing import Any

import pytest
import requests

HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/"),
        ("GET", "/not_found"),
        ("POST", "/"),
        ("POST", "/not_found"),
    ],
)
def test_not_found(method: str, path: str):
    response = requests.request(method, BASE_URL + path)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ("query", "status_code", "result"),
    [
        ({"n": ""}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"n": "lol"}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"x": "kek"}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({"n": -1}, HTTPStatus.BAD_REQUEST, None),
        ({"n": 0}, HTTPStatus.OK, 1),
        ({"n": 1}, HTTPStatus.OK, 1),
        ({"n": 10}, HTTPStatus.OK, 3628800),
    ],
)
def test_factorial(query: dict[str, Any], status_code: int, result: int | None):
    response = requests.get(BASE_URL + "/factorial", params=query)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        assert "result" in response.json()
        assert result == response.json()["result"]


@pytest.mark.parametrize(
    ("params", "status_code", "result"),
    [
        ("/lol", HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ("/-1", HTTPStatus.BAD_REQUEST, None),
        ("/0", HTTPStatus.OK, 0),
        ("/1", HTTPStatus.OK, 1),
        ("/10", HTTPStatus.OK, 55),
    ],
)
def test_fibonacci(params: str, status_code: int, result: int | None):
    response = requests.get(BASE_URL + "/fibonacci" + params)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        assert "result" in response.json()
        assert result == response.json()["result"]


@pytest.mark.parametrize(
    ("json", "status_code", "result"),
    [
        (None, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ([], HTTPStatus.BAD_REQUEST, None),
        ([1, 2, 3], HTTPStatus.OK, 2.0),
        ([1, 2.0, 3.0], HTTPStatus.OK, 2.0),
        ([1.0, 2.0, 3.0], HTTPStatus.OK, 2.0),
    ],
)
def test_mean(json: dict[str, Any] | None, status_code: int, result: float | None):
    response = requests.get(BASE_URL + "/mean", json=json)

    assert response.status_code == status_code
    if status_code == HTTPStatus.OK:
        assert "result" in response.json()
        assert result == response.json()["result"]
