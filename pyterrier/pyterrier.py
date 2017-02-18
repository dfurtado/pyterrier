import os, sys, re
from socketserver import TCPServer

from .serializers import JsonSerializer
from .renderers  import Jinja2TemplateRenderer

from .core.http_handlers  import HttpRequestHandler
from .core.route_converter import DefaultRouteConverter
from .core.threaded_server import ThreadedServer

class PyTerrier():
    def __init__(
            self,
            hostname="localhost",
            port=8000,
            template_dir=os.path.join(os.path.dirname(sys.argv[0]), 'templates'),
            static_files=os.path.join(os.path.dirname(sys.argv[0]), 'static'),
            renderer=Jinja2TemplateRenderer,
            route_converter=DefaultRouteConverter):
        """
        Create a new server.
        :param hostname: The hostname the server will be created.
        :param port: Which port the server will listen for connections.
        :param template_dir: Folder where to find the site templates.
        :param static_files: Folder that will contain all static files, images, stylesheets, fonts.

        Example:

        from pyterrier.core import PyTerrier
        from pyterrier.decorators import jsonresponse

        app = Pyterrier()

        @app.get('/users/{id:int}')
        @jsonresponse
        def get_user(id):
            return user_datarepo.get(id)

        @app.get('/')
        def index():
            return app.view_result(name = "index.html")

        @app.post('/user/save')
        def save_action(formdata):

        _context = {
            "field1": formdata['field1'],
            "field2": formdata['field2'],
            "field3": formdata['field3'],
        }

        return app.view_result(name="template.html", context = _context)

        if __name__ == '__main__':
            app.run()

        """

        self._hostname = hostname
        self._port = port
        self._template_dir = template_dir
        self._static_files = static_files

        self._renderer = renderer(self._template_dir)

        self.route_table = {}

        self.route_converter = route_converter()

    def view_result(self, name, context={}):
        """ Returns the rendered template """

        return self._renderer.get_template(name, context)

    def json_result(self, data={}, json_serializer=JsonSerializer):
        """ Returns the result in json format """
        response = json_serializer.serialize(result)
        return


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

        _handler = lambda *args: HttpRequestHandler(
            self.route_table,
            {'templates': self._template_dir, 'staticfiles': self._static_files,},
            *args)

        self.print_config()
        self._server = ThreadedServer((self._hostname, self._port), _handler)
        self._server.serve_forever()

    def _register_route(self, route, verb, func):
        """ Register a new route, duplicate routes will be overwritten"""

        r = self.route_converter.convert(route)
        self.route_table.update({r: (verb, func)})

    def page_not_found(self, route="/pagenotfound"):
        """ Default page not found response """

        return lambda func: self._register_route(route, 'GET', func)

    def get(self, route):
        """ Decorator for GET actions."""

        return lambda func: self._register_route(route, 'GET', func)

    def post(self, route):
        """ Decorator for POST actions """

        return lambda func: self._register_route(route, 'POST', func)

    def put(self, route):
        """ Decorator for PUT actions """

        return lambda func: self._register_route(route, 'PUT', func)

    def delete(self, route):
        """ Decorator for DELETE actions """

        return lambda func: self._register_route(route, 'DELETE', func)
