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

                response = None

                if isinstance(results, ViewResult):
                    response = self._prepare_view_result(results)

                elif isinstance(results, HttpResult):
                    response = self._prepare_json_result(results)

                self.prepare_response(*response)

            else:
                self._serve_file(self.path)

        except KeyError as e:
            """ TODO: change this exception it doesn't make any fucking sense. """
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))

    def _prepare_view_result(self, view_result):
        """
        Render the view result returning the rendered view using the default
        template engine.

        view_result: It is an instance of HttpResult that is the
                     result of the requested action.
        """

        response = ()

        try:
            response = (
                    self._renderer.render(view_result.template, view_result.context),
                    HTTPStatus.OK,
                    "text/html",
                    )
        except Exception as e:
            """ TODO: It should return a default error page here rather than JSON """
            response = (
                    str(e),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "application/json",
                    )

        return response

    def _prepare_json_result(self, json_result):
        """
        Parse the json result returning a prepare response to be sent
        to the client.
        The response will be a tuple containing: (HTTPStatus, data, content-type)

        json_result: It is a instance of HttpResult that is result of the
                     request action.
        """

        response = ()

        try:
            response = (
                    json.dumps(json_result.data, cls=DefaultJsonEncoder),
                    json_result.http_status,
                    "application/json",
                    )

        except TypeError as e:
            response = (
                    str(e),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "application/json",
                    )

        return response


    def get_mime_type(self, path):
        """
        Retuns the mime type base on the extension of the file that the client is
        requesting.

        path: The relative path to the static file, it will by default search in the
              static folder in the application root.
        """

        match = self._static_regex.search(path)

        if  match != None and match.group("ext") != None:
            return mimetypes.types_map[match.group("ext")]


    def _serve_file(self, path):
        """
        Server a static file to the client.

        path: The relative path to the static file, it will by default search in the
              static folder in the application root.
        """

        path = os.path.normpath(self._config['staticfiles'] + self.path)

        mime_type = self.get_mime_type(path)

        if mime_type == None:
            self.prepare_response("Unsupported media type.", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        if not os.path.exists(path):
            self.prepare_response("File not found.", HTTPStatus.NOT_FOUND)
        else:
            with open(path, encoding = "ISO-8859-1") as f:
                results = f.read()
                self.prepare_response(results, HTTPStatus.OK, mime_type)
