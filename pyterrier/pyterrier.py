import os
import sys
import re

from socketserver import TCPServer
from typing import List, Tuple, Any, Optional

from .http.http_handler  import HttpRequestHandler
from .core.route_converter import RouteConverter
from .core.threaded_server import ThreadedServer
from .core.route_discovery import RouteDiscovery
from .renderers.jinja2TemplateRenderer  import Jinja2TemplateRenderer

from typing import Dict, Callable

class PyTerrier():
    def __init__(
            self,
            hostname: Optional[str]="localhost",
            port: Optional[int]=8000,
            template_dir: Optional[str]=os.path.join(os.path.dirname(sys.argv[0]), 'templates'),
            static_files: Optional[str]=os.path.join(os.path.dirname(sys.argv[0]), 'static'),
            renderer=Jinja2TemplateRenderer) -> None:
        """
        Create a new server.

        :Parameters:

        - `hostname` (optional): The hostname the server will be created.
        - `port` (optional): Which port the server will listen for connections.
        - `template_dir` (optional): Folder where to find the site templates.
        - `static_files` (optional): Folder that will contain all static files, images, stylesheets, fonts.
        - `renderer` (optional): Specify the default template engine that will be used by the framework.

        :Usage:

        from pyterrier import PyTerrier
        from pyterrier.http import HttpResponse
        from http import HTTPStatus

        app = Pyterrier()

        @app.get('/users/{id:int}')
        def get_user(id):
            user = user_datarepo.get(id)
            return HttpResponse(user, HTTPStatus.OK)

        @app.get('/')
        def index():
            return ViewResult(name = "index.html")

        @app.post('/user/save')
        def save_action(formdata):
            _context = {
                "field1": formdata['field1'],
                "field2": formdata['field2'],
                "field3": formdata['field3'],
            }

            return ViewResult(name="template.html", context = _context)

        if __name__ == '__main__':
            app.run()
        """

        self._hostname = hostname
        self._port = port

        self._template_dir = template_dir
        self._static_files = static_files

        self._route_discovery = RouteDiscovery()
        self.route_converter = RouteConverter()
        self._route_table: Dict[str, Tuple[str, Any]] = {}

        self._renderer = renderer(self._template_dir)


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

        handler = lambda *args: HttpRequestHandler(
                self._route_table, options, self._renderer,*args)

        self._print_config()
        self._server = ThreadedServer((self._hostname, self._port), handler)
        self._server.serve_forever()


    def init_routes(self, prefix_routes=False):
        """
        The init_routes function will get all routes and actions that have been
        created in files in the controllers folder and register within the
        PyTerrier route table.

        :Parameters:

        - `prefix_routes` (optional): Tell the framework to prefix the route with the
        name of the controller.

        .. Notes:: `controllers` are defined in the controllers directory in the
        application's root directory. For instance, if the application has a controller
        named `userController.py` and for this controller there's a action defined with
        the route /get/{id:int}, if `init_route` is called with the parameter `prefix_route`
        set to `True`, the action will be registered as /user/get/{id:int}

        :Usage:

        app = PyTerrier()
        app.init_routes()
        """

        self._route_discovery.register_actions(prefix_routes)

        for route in self._route_discovery.actions:
            self._register_route(*route)


    def _register_route(self, route: str, verb: str, func):
        """
        Register a new route.

        :Parameters:
        - `route`: the route definition
        - `verb`: the HTTP verb that the action will respond to.
        - `func`: the function that will be invoked when the route is
        accessed.

        .. Note:: Duplicated routes will be overwritten.
        """
        func.__setattr__('request', None)
        action = func.__get__(func, type(func))

        r = self.route_converter.convert(route)
        self._route_table.update({r: (verb, action)})


    def page_not_found(self, route="/pagenotfound"):
        """
        Default page not found response
        :param route - Specify the route where the 404 view will be placed, default is /pagenotfound
        """

        return lambda func: self._register_route(route, 'GET', func)


    def get(self, route):
        """
        Decorator for GET actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the decorator @get in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        """

        return lambda func: self._register_route(route, 'GET', func)


    def post(self, route):
        """
        Decorator for POST actions

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @post decorator in pyterrier.http.post module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        """

        return lambda func: self._register_route(route, 'POST', func)


    def put(self, route):
        """
        Decorator for PUT actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @put decorator in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        """

        return lambda func: self._register_route(route, 'PUT', func)


    def delete(self, route):
        """
        Decorator for DELETE actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @delete decorator in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        """

        return lambda func: self._register_route(route, 'DELETE', func)
