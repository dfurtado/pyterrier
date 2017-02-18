from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import os, re, mimetypes, cgi

from .route_resolver import RouteResolver

class HttpRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, route_table, config, *args):
       """
       Create a new request handler.
       :param route_table: A dict with route information, the key is the route as string and
                           the value is a tuple containing the http verb and the action to be
                           executed when the route is requested.
       """

       self._route_table = route_table
       self._resolver = RouteResolver(route_table)
       self._config = config

       self._static_regex = re.compile("/\w+(?P<ext>.\w{3,4})$", re.IGNORECASE | re.DOTALL)

       BaseHTTPRequestHandler.__init__(self, *args)

       mimetypes.init()

    def _fileResponse(self, path, match):
        """ Read the contents of a requested file and send it to the client """

        with open(path, encoding = "ISO-8859-1") as f:
            results = f.read()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", mimetypes.types_map[match.group("ext")])
            self.end_headers()
            self.wfile.write(bytes(results, "ISO-8859-1"))

    def ok_response(self, results, content_type="text/html"):
        """ Send a 200 HTTP response back to the client """

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(bytes(results, "ISO-8859-1"))

    def _decodeResults(self, data):
        """ Decode the binary strings to utf-8 """

        return { x[0].decode('utf-8'):x[1][0].decode('utf-8') for x in data.items() }

    def do_POST(self):
        """
            Handler POST requests
            At the moment, only data posted by forms are being handled.
            For file uploads need to create the uploaded file to a
            temporary location.
        """

        try:

            action_info = self._resolver.resolve(self.path)

            ctype, pdict = cgi.parse_header(self.headers.get_content_type())

            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.get('Content-Length'))
                postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}

            if(action_info != None):
                verb, handler, params = action_info
                decoded_str = self._decodeResults(postvars)
                results = handler(decoded_str)
                self.ok_response(results)

        except KeyError as e:
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))


    def do_GET(self):
        """
        Handle all post requests.
        It will get a request path and search for it in the route table.
        If the action for the request is found it will be executed and the response
        will be returned.
        """

        try:

            action_info = self._resolver.resolve(self.path)

            if action_info != None:
                (verb, handler, params) = action_info
                results = handler(*params)
                self.ok_response(results)
            else:
                m = self._static_regex.search(self.path)

                if m != None and m.group("ext") != None:
                    path = os.path.normpath(self._config['staticfiles'] + self.path)
                    if os.path.exists(path):
                        self._fileResponse(path, m)
                    else:
                        self.send_response(HTTPStatus.NOT_FOUND)
                else:
                    self.send_response(HTTPStatus.NOT_FOUND)

        except KeyError as e:
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))


