from http.server import BaseHTTPRequestHandler,HTTPServer
import binascii

class test:
    def show(self):
        return "aaaa"

class http_server:
    def __init__(self, t1):
        def handler(*args):
            myHandler(t1, *args)
        server = HTTPServer(('', 8080), handler)
        server.serve_forever()

class myHandler(BaseHTTPRequestHandler):
    def __init__(self, t1, *args):
        self.t1 = t1
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(self.t1.show(), "ascii")) #Doesnt work
        return

class main:
    def __init__(self):
        self.t1 = test()

        self.server = http_server(self.t1)

if __name__ == '__main__':
    m = main()
