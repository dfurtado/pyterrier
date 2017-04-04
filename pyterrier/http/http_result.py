from http import HTTPStatus
from typing import Optional


class HttpResult:
    """
    Represents the data to be returned to the client
    as a response of a http request.
    By default data in this object will be serialized
    to JSON using the default JSON serializer.
    """

    def __init__(self, data, http_status: Optional[int]=HTTPStatus.OK) -> None:
        self._data = data
        self._http_status = http_status

    @property
    def http_status(self):
        return self._http_status

    @property
    def data(self):
        return self._data
