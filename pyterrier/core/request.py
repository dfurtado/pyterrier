from http import cookies
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Request:
    """
    Class representing a HTTP request.
    """

    def __init__(self, request):
        self.path = urlparse(request.path).path
        self.requestline = request.requestline
        self.headers = {k: v for (k, v) in request.headers.items()}
        self.params = self._parse_params(request)
        self.cookies = cookies.SimpleCookie()
        self.method = request.requestline.split(' ')[0]

        try:
            self.cookies.load(self.headers['Cookie'])
        except KeyError:
            self.cookies = None

    def _parse_params(self, request):
        query = urlparse(request.path).query
        return parse_qs(query)
