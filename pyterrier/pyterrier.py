import sys
import re

from os.path import join
from os.path import dirname

from typing import Tuple
from typing import Any
from typing import Optional
from typing import Dict
from typing import List

from .http.http_handler import HttpRequestHandler
from .core.route_converter import RouteConverter
from .core.threaded_server import ThreadedServer
from .core.route_discovery import RouteDiscovery
from .renderers.jinja2_renderer import Jinja2Renderer
from .renderers.base_renderer import BaseRenderer


class PyTerrier():

    def __init__(
            self,
            hostname: Optional[str]='localhost',
            port: Optional[int]=8000,
            template_dir: Optional[str]='templates',
            static_files: Optional[str]='static',
            renderer: Optional[BaseRenderer]=Jinja2Renderer) -> None:
        """
        Create a new PyTerrier application

        :Parameters:

        - `hostname`: The hostname the server will be created.
        - `port`: Which port the server will listen for connections.
        - `template_dir`: Folder where to find the site templates.
        - `static_files`: Folder that will contain all static files, images,
        stylesheets, fonts.
        - `renderer`: Specify the default template engine that will be used
        by the framework.
        """

        if not issubclass(renderer, BaseRenderer):
            error_msg = ('The parameter `renderer` needs to be a subclass of '
                         'pyterrier.renderers.BaseTemplateRenderer')
            raise TypeError(error_msg)

        self._hostname = hostname
        self._port = port

        self._template_dir = join(dirname(sys.argv[0]), template_dir)
        self._static_files = join(dirname(sys.argv[0]), static_files)

        self._route_discovery = RouteDiscovery()
        self.route_converter = RouteConverter()
        self._route_table: Dict[str, Tuple[str, Any]] = {}

        self._renderer = renderer(self._template_dir)

    def _print_config(self) -> None:
        """ Print the server information. """

        print(f'Server started at http://{self._hostname}:{self._port}')
        print(f'=> template_dir: {self._template_dir}')
        print(f'=> static_dir: {self._static_files}')

    def run(self) -> None:
        """
        Start the server and listen on the specified port
        for new connections.
        """

        options = {
            'templates': self._template_dir,
            'staticfiles': self._static_files
        }

        def _handler(*args):
            return HttpRequestHandler(
                self._route_table,
                options,
                self._renderer,
                *args
            )

        self._print_config()
        self._server = ThreadedServer((self._hostname, self._port), _handler)

        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            print('\nStopping server. Bye!')

    def init_routes(self, prefix_routes: Optional[bool]=False) -> None:
        """
        The init_routes function will get all routes and actions that have been
        created in files in the controllers folder and register within the
        PyTerrier route table.

        :Parameters:

        - `prefix_routes`: Tell the framework to prefix the route with the
        name of the controller.

        .. Notes:: `controllers` are defined in the controllers directory in
        the application's root directory. For instance, if the application
        has a controller named `userController.py` and for this controller
        there's a action defined with the route /get/{id:int}, if `init_route`
        is called with the parameter `prefix_route` set to `True`, the action
        will be registered as /user/get/{id:int}

        :Usage:

        app = PyTerrier()
        app.init_routes()
        """

        self._route_discovery.register_actions(prefix_routes)

        for route in self._route_discovery.actions:
            self._register_route(*route)

    def _register_route(
            self,
            route: str,
            default_method: str,
            func,
            additional_methods: List[str]=[]):
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

        uri_regex = self.route_converter.convert(route)
        compiled_uri_regex = re.compile(uri_regex)

        methods = [default_method] + additional_methods

        for method in methods:
            if self._route_table.get(method, None):
                self._route_table[method].append((compiled_uri_regex, action))
            else:
                self._route_table[method] = [(compiled_uri_regex, action)]

    def get(self, route: str, additional_methods: List[str]=[]):
        """
        Decorator for GET actions.

        :Parameters:
        - `route`: the URL where the decorated function (action)
        can be invoked.

        .. Note:: This decorator has the same functionality as the decorator
        @get in pyterrier.http module, the main difference is that this
        decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created. If you intend to define
        the actions in files in the `controllers` folder use pyterrier.http.get
        instead.

        .. Usage::
        @app.get('/api/get')
        def get(self):
            ...
        """

        return lambda func: self._register_route(
            route, 'GET', func, additional_methods
        )

    def post(self, route: str, additional_methods: List[str]=[]):
        """
        Decorator for POST actions

        :Parameters:
        - `route`: the URL where the decorated function (action) can be
        invoked.

        .. Note:: This decorator has the same functionality as the @post
        decorator in pyterrier.http.post module, the main difference is that
        this decorator are meant to be used when defining actions in the same
        file where the instance of PyTerrier is created. If you intend to
        define the actions in files in the `controllers` folder use
        pyterrier.http.post instead.

        .. Usage::
        @app.post('/api/add')
        def post(self):
            ...
        """

        return lambda func: self._register_route(
            route, 'POST', func, additional_methods
        )

    def put(self, route: str, additional_methods: List[str]=[]):
        """
        Decorator for PUT actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be
        invoked.

        .. Note:: This decorator has the same functionality as the @put
        decorator in pyterrier.http module, the main difference is that this
        decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers`
        folder use pyterrier.http.put instead.

        .. Usage::
        @app.put('/api/update')
        def put(self):
            ...
        """

        return lambda func: self._register_route(
            route, 'PUT', func, additional_methods
        )

    def patch(self, route: str, additional_methods: List[str]=[]):
        """
        Decorator for PATCH actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be
        invoked.

        .. Note:: This decorator has the same functionality as the @patch
        decorator in pyterrier.http module, the main difference is that this
        decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created.
        If you intend to define the actions in files in the `controllers`
        folder use pyterrier.http.patch instead.

        .. Usage::
        @app.patch('/api/update')
        def patch(self):
            ...
        """

        return lambda func: self._register_route(
            route, 'PATCH', func, additional_methods
        )

    def delete(self, route: str, additional_methods: List[str]=[]):
        """
        Decorator for DELETE actions.

        :Parameters:
        - `route`: the URL where the decorated function (action) can be
        invoked.

        .. Note:: This decorator has the same functionality as the @delete
        decorator in pyterrier.http module, the main difference is that this
        decorator are meant to be used when defining actions in the same file
        where the instance of PyTerrier is created. If you intend to define
        the actions in files in the `controllers` folder use
        pyterrier.http.delete instead.

        .. Usage::
        @app.delete('/api/delete')
        def delete(self):
            ...
        """

        return lambda func: self._register_route(
            route, 'DELETE', func, additional_methods
        )
