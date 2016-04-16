from http.server import BaseHTTPRequestHandler


class PyTerrierRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, route_table, *args):
       self._route_table = route_table
       BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_GET(self):
        
        (verb, handler) = self._route_table[self.path]
        results =  handler()

        self.send_response(200)
        self.send_header("Content-type:", "text/html")
        self.end_headers()
        self.wfile.write(bytes(results, "ascii"))
