from http import HTTPStatus
from typing import Any

from .http_result import HttpResult


def Ok(data: Any={}):
    return HttpResult(data, HTTPStatus.OK)


def NotFound():
    return HttpResult({}, HTTPStatus.NOT_FOUND)


def NoContent():
    return HttpResult({}, HTTPStatus.NO_CONTENT)
