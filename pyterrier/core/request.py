from urllib import parse_url, parse_qs

class Request:

    def __init__(self, request):
        self._http_verb = http_verb
        self._path = path
        self._request_string = request_string
        self._query_string = query_string
        self._headers = headers


    @property
    def http_verb(self):
        return self._http_verb


    @property
    def path(self):
        return self._path


    @property
    def request_string(self):
        return self._request_string


    @property
    def query_string(self):
        return self._query_string


    @property
    def headers(self):
        return self._headers
