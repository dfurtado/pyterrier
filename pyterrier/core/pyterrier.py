import os, sys
from socketserver import TCPServer
from .server import PyTerrierRequestHandler
from .renderers.jinja2TemplateRenderer import Jinja2TemplateRenderer


class PyTerrier():

    def __init__(
            self,
            hostname="localhost",
            port=8000,
            template_dir=os.path.join(os.path.dirname(sys.argv[0]), 'templates'),
            static_files="static",
            renderer=Jinja2TemplateRenderer):
        """
        Create a new server.
        :param hostname: The hostname the server will be created.
        :param port: Which port the server will listen for connections.
        :param template_dir: Folder where to find the site templates.
        :param static_files: Folder that will contain all static files, images, stylesheets, fonts.
        """
        self._hostname = hostname
        self._port = port
        self._template_dir = template_dir
        self._static_files = static_files

        self._renderer = renderer(self._template_dir)

        self.route_table = {}


    def get_template(self, name):
        """ Returns the rendered template """

        return self._renderer.get_template(name)


    @property
    def template_dir(self):
        """ Return the current template directory """

        return self._template_dir


    @property
    def static_files(self):
        """ Returns the current static files directory """

        return self._static_files


    def print_config(self):
        """ Print the server configuration. """

        print("Server started at http://{host}:{port}".format(host=self._hostname, port=self._port))
        print("=> template_dir: {template_dir}".format(template_dir=self.template_dir))
        print("=> static_dir: {static_files}".format(static_files=self.static_files))


    def run(self):
        """ Start the server and listen on the specified port for new connections."""

        _handler = lambda *args: PyTerrierRequestHandler(self.route_table, *args)

        self.print_config()
        self._server = TCPServer((self._hostname, self._port), _handler)
        self._server.serve_forever()


    def _register_route(self, route, verb, func):
        """Register a new route, duplicate routes will be overwritten"""

        print("Registering : {r}".format(r = route))
        self.route_table.update({ route: (verb, func) })


    def get(self, route):
        """ Decorator for GET actions."""

        return lambda func: self._register_route(route,'GET', func)


    def post(self, route):
        """ Decorator for POST actions"""

        return lambda func: self._register_route(route,'POST', func)


    def put(self, route):
        """ Decorator for PUT actions"""

        return lambda func: self._register_route(route,'PUT', func)


    def delete(self, route):
        """ Decorator for DELETE actions"""

        return lambda func: self._register_route(route,'DELETE', func)
