from http.server import BaseHTTPRequestHandler
from .resolver import RouteResolver

class PyTerrierRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, route_table, *args):
       """
       Create a new request handler.
       :param route_table: A dict with route information, the key is the route as string and
                           the value is a tuple containing the http verb and the action to be
                           executed when the route is requested.       """

       self._route_table = route_table
       self._resolver = RouteResolver(route_table)

       BaseHTTPRequestHandler.__init__(self, *args)


    def do_GET(self):
        """
        Handle all post requests.
        It will get a request path and search for it in the route table.
        If the action for the request is found it will be executed and the response
        will be returned.
        """
        try:
            (verb, handler, params) = self._resolver.resolve(self.path)
            results = handler(params)

            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))

        except KeyError as e:
            (verb, handler) = self._route_table["/pagenotfound"]
            results = handler()

            self.send_response(404)
            self.send_header("Content-type:", "text/html")
            self.end_headers()
            self.wfile.write(bytes(results, "ascii"))


