from http.server import BaseHTTPRequestHandler
#from http import HTTPStatus
from .resolver import RouteResolver
import os, re, mimetypes

class PyTerrierRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, route_table, config, *args):
       """
       Create a new request handler.
       :param route_table: A dict with route information, the key is the route as string and
                           the value is a tuple containing the http verb and the action to be
                           executed when the route is requested.       """

       self._route_table = route_table
       self._resolver = RouteResolver(route_table)
       self._config = config

       self._static_regex = re.compile("/\w+(?P<ext>.\w{3,4})$", re.IGNORECASE | re.DOTALL)

       BaseHTTPRequestHandler.__init__(self, *args)

       mimetypes.init()

    def _fileResponse(self, path, match):
        with open(path, encoding = "ISO-8859-1") as f:
            results = f.read()
            self.send_response(200)
            self.send_header("Content-type", mimetypes.types_map[match.group("ext")])
            self.end_headers()
            self.wfile.write(bytes(results, "ISO-8859-1"))

    def _actionResponse(self, action_info):
        (verb, handler, params) = action_info
        results = handler(*params)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(results, "ISO-8859-1"))

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
              self._actionResponse(action_info)
            else:
                m = self._static_regex.search(self.path)

                if m != None and m.group("ext") != None:
                    path = os.path.normpath(self._config['staticfiles'] + self.path)
                    if os.path.exists(path):
                        self._fileResponse(path, m)
                    else:
                         self.send_response(404)
                else:
                    self.send_response(404)

        except KeyError as e:
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))


