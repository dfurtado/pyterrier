from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import os, re, mimetypes, cgi, json

from .view_result import ViewResult
from .http_result import HttpResult

from pyterrier.core.route_resolver import RouteResolver

from pyterrier.encoders.default_json_encoder import DefaultJsonEncoder

class HttpRequestHandler(BaseHTTPRequestHandler):
    """
    Le framework's HTTP handler.
    """


    def __init__(self, route_table, config, renderer, *args):
       """
       Create a new request handler.
       :param route_table: A dict with route information, the key is the route as string and
                           the value is a tuple containing the http verb and the action to be
                           executed when the route is requested.
       """

       self._route_table = route_table
       self._resolver = RouteResolver(route_table)
       self._config = config
       self._renderer = renderer

       self._static_regex = re.compile("/\w+(?P<ext>.\w{3,4})$", re.IGNORECASE | re.DOTALL)

       BaseHTTPRequestHandler.__init__(self, *args)

       mimetypes.init()


    def prepare_response(self, results, http_status, content_type="text/html"):
        """ Prepare response to be sent to the client """

        self.send_response(http_status)
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
                self.prepare_response(results)

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

                content_type = None

                if isinstance(results, ViewResult):
                    content = (results.template, results.context)
                    results = self._renderer.render(*content)
                elif isinstance(results, HttpResult):
                    results = json.dumps(results.data, cls=DefaultJsonEncoder)
                    content_type = "application/json"

                self.prepare_response(results, HTTPStatus.OK, content_type)

            else:
                self._serve_file(self.path)

        except KeyError as e:
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))


    def get_mime_type(self, path):
        match = self._static_regex.search(path)

        if  match != None and match.group("ext") != None:
            return mimetypes.types_map[match.group("ext")]


    def _serve_file(self, path):

        path = os.path.normpath(self._config['staticfiles'] + self.path)

        mime_type = self.get_mime_type(path)

        if mime_type == None:
            self.send_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        if not os.path.exists(path):
            self.send_response(HTTPStatus.NOT_FOUND)

        try:
            with open(path, encoding = "ISO-8859-1") as f:
                results = f.read()
                self.prepare_response(results, HTTPStatus.OK, mime_type)
        except:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
