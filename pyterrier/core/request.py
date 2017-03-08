from urllib.parse import urlparse, parse_qs

class Request:

    def __init__(self, request):
        self._path = urlparse(request.path).path
        self._requestline = request.requestline
        self._headers = {k:v for (k,v) in request.headers.items()}
        self._params = self._parse_params(request)
            

    @property
    def params(self):
        return self._params


    @property
    def path(self):
        return self._path


    @property
    def requestline(self):
        return self._requestline


    @property
    def headers(self):
        return self._headers


    def _parse_params(self, request):
        query = urlparse(request.path).query
        return parse_qs(query)
