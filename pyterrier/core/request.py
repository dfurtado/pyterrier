from urllib.parse import urlparse, parse_qs
from typing import Iterator, Dict

class Request:
    """
    Class representing a HTTP request.
    """

    def __init__(self, request):
        self._path = urlparse(request.path).path
        self._requestline = request.requestline
        self._headers = {k: v for (k, v) in request.headers.items()}
        self._params = self._parse_params(request)

    @property
    def params(self) -> Iterator[object]:
        return self._params

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
