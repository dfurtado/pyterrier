import sys
import re

from socketserver import TCPServer
from os.path import join, dirname
from typing import List, Tuple, Any, Optional, Dict, Callable

from .http.http_handler  import HttpRequestHandler
from .core.route_converter import RouteConverter
from .core.threaded_server import ThreadedServer
from .core.route_discovery import RouteDiscovery
from .renderers.jinja2TemplateRenderer  import Jinja2TemplateRenderer
from .renderers.baseTemplateRenderer import BaseTemplateRenderer

class PyTerrier():
    def __init__(
            self,
            hostname: Optional[str]="localhost",
            port: Optional[int]=8000,
            template_dir: Optional[str]=join(dirname(sys.argv[0]), 'templates'),
            static_files: Optional[str]=join(dirname(sys.argv[0]), 'static'),
            renderer: Optional[BaseTemplateRenderer]=Jinja2TemplateRenderer) -> None:
        """
        Create a new PyTerrier application

        :Parameters:

        - `hostname`: The hostname the server will be created.
        - `port`: Which port the server will listen for connections.
        - `template_dir`: Folder where to find the site templates.
        - `static_files`: Folder that will contain all static files, images, stylesheets, fonts.
        - `renderer`: Specify the default template engine that will be used by the framework.
        """

        if not issubclass(renderer, BaseTemplateRenderer):
            raise TypeError("The parameter `renderer` needs to be a subclass of pyterrier.renderers.BaseTemplateRenderer")

        self._hostname = hostname
        self._port = port

        self._template_dir = template_dir
        self._static_files = static_files

        self._route_discovery = RouteDiscovery()
        self.route_converter = RouteConverter()
        self._route_table: Dict[str, Tuple[str, Any]] = {}

        self._renderer = renderer(self._template_dir)


    def _print_config(self) -> None:
        """
        Print the server information.
        """

        print(f"Server started at http://{self._hostname}:{self._port}")
        print(f"=> template_dir: {self._template_dir}")
        print(f"=> static_dir: {self._static_files}")


    def run(self) -> None:
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


    def init_routes(self, prefix_routes: bool=False) -> None:
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

    def get(self, route: str):
        """
        Decorator for GET actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the decorator @get in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers` folder use pyterrier.http.get instead.

        .. Usage::
        @app.get("/api/get")
        def get(self):
            pass
        """

        return lambda func: self._register_route(route, 'GET', func)

    def post(self, route: str):
        """
        Decorator for POST actions

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @post decorator in pyterrier.http.post module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers` folder use pyterrier.http.post instead.

        .. Usage::
        @app.post("/api/add")
        def post(self):
            pass
        """

        return lambda func: self._register_route(route, 'POST', func)

    def put(self, route: str):
        """
        Decorator for PUT actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @put decorator in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers` folder use pyterrier.http.put instead.

        .. Usage::
        @app.put("/api/add")
        def put(self):
            pass
        """

        return lambda func: self._register_route(route, 'PUT', func)

    def delete(self, route: str):
        """
        Decorator for DELETE actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be invoked.

        .. Note:: This decorator has the same functionality as the @delete decorator in pyterrier.http module, the main
        difference is that this decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers` folder use pyterrier.http.delete instead.

        .. Usage::
        @app.delete("/api/delete")
        def delete(self):
            pass
        """

        return lambda func: self._register_route(route, 'DELETE', func)
