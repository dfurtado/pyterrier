from http import cookies
from urllib.parse import urlparse
from urllib.parse import parse_qs
from typing import Iterator
from typing import Dict


class Request:
    """
    Class representing a HTTP request.
    """

    def __init__(self, request):
        self._path = urlparse(request.path).path
        self._requestline = request.requestline
        self._headers = {k: v for (k, v) in request.headers.items()}
        self._params = self._parse_params(request)
        self._cookies = cookies.SimpleCookie()

        try:
            self._cookies.load(self._headers['Cookie'])
        except KeyError:
            self._cookies = None

    @property
    def params(self) -> Iterator[object]:
        return self._params

    @property
    def cookies(self):
        return self._cookies

    @property
    def path(self) -> str:
        return self._path

    @property
    def requestline(self) -> str:
        return self._requestline

    @property
    def headers(self) -> Dict:
        return self._headers

    def _parse_params(self, request):
        query = urlparse(request.path).query
        return parse_qs(query)
