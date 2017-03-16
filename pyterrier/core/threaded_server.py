from http.server import HTTPServer
from socketserver import ThreadingMixIn


class ThreadedServer(ThreadingMixIn, HTTPServer):
    pass
