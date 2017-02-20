import os, sys, re
from socketserver import TCPServer

from .serializers import JsonSerializer
from .renderers  import Jinja2TemplateRenderer

from .core.http_handlers  import HttpRequestHandler
from .core.route_converter import RouteConverter
from .core.threaded_server import ThreadedServer
from .core.route_discovery import RouteDiscovery

class PyTerrier():
    def __init__(
            self,
            hostname="localhost",
            port=8000,
            template_dir=os.path.join(os.path.dirname(sys.argv[0]), 'templates'),
            static_files=os.path.join(os.path.dirname(sys.argv[0]), 'static'),
            renderer=Jinja2TemplateRenderer):
        """
        Create a new server.
        :param hostname: The hostname the server will be created.
        :param port: Which port the server will listen for connections.
        :param template_dir: Folder where to find the site templates.
        :param static_files: Folder that will contain all static files, images, stylesheets, fonts.
        :param renderer: Specify the default template engine that will be used by the framework.

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
        self._route_discovery = RouteDiscovery()
        self._renderer = renderer(self._template_dir)

        self._route_table = {}

        self.route_converter = RouteConverter()


    def view_result(self, name, context={}):
        """
        Returns the rendered template
        """

        return self._renderer.get_template(name, context)

    def json_result(self, data={}, json_serializer=JsonSerializer):
        """
        Returns the result in json format
        """

        response = json_serializer.serialize(result)
        return


    @property
    def template_dir(self):
        """
        Return the current template directory.
        """

        return self._template_dir

    @property
    def static_files(self):
        """
        Returns the current static files directory.
        """

        return self._static_files

    def _print_config(self):
        """
        Print the server information.
        """

        print(f"Server started at http://{self._hostname}:{self._port}")
        print(f"=> template_dir: {self._template_dir}")
        print(f"=> static_dir: {self._static_files}")


    def run(self):
        """
        Start the server and listen on the specified port for new connections.
        """

        options = {
            "templates": self._template_dir,
            "staticfiles": self._static_files
        }

        handler = lambda *args: HttpRequestHandler(self._route_table, options, *args)

        self._print_config()
        self._server = ThreadedServer((self._hostname, self._port), handler)
        self._server.serve_forever()


    def init_routes(self, prefix_routes=False):
        """
        The init_routes function will get all routes and actions that have been
        created in files in the controllers folder and register within the
        PyTerrier route table.

        Usage:
            app = PyTerrier()
            app.init_routes()

        There's also an optional boolean parameter prefix_routes which tells PyTerrier
        to prefix the route with the name of the controller, for instance, if there's a file
        named userController in the controllers folder with the content bellow:

        @get("/getuser/{id:int}")
        def get_users(id):
            user = user_repository.get_user(id)
            return json_result(user)

        If the prefix_routes is set to True the route will be created as
        /user/getuser/{id:int}, if it is not set or False the route will be /getuser/{id:int}
        """

        self._route_discovery.register_actions(prefix_routes)

        for route in self._route_discovery.actions:
            self._register_route(*route)


    def _register_route(self, route, verb, func):
        """
        Register a new route, duplicate routes will be overwritten
        """

        r = self.route_converter.convert(route)
        self._route_table.update({r: (verb, func)})

    def page_not_found(self, route="/pagenotfound"):
        """
        Default page not found response
        :param route - Specify the route where the 404 view will be placed, default is /pagenotfound
        """

        return lambda func: self._register_route(route, 'GET', func)

    def get(self, route):
        """
        Decorator for GET actions.
        """

        return lambda func: self._register_route(route, 'GET', func)

    def post(self, route):
        """
        Decorator for POST actions
        """

        return lambda func: self._register_route(route, 'POST', func)

    def put(self, route):
        """
        Decorator for PUT actions
        """

        return lambda func: self._register_route(route, 'PUT', func)

    def delete(self, route):
        """
        Decorator for DELETE actions
        """

        return lambda func: self._register_route(route, 'DELETE', func)
