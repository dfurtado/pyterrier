import os
import re


class RouteDiscovery:
    """
    Get all files in the default controllers folder, import all the
    files and register it actions.
    """

    def __init__(self):
        self._actions = []
        self.controllers = []
        self._controller_folder = 'controllers'
        self._recontroller = re.compile(r'[\w\-]+(Controller)$')

    @property
    def actions(self):
        """
        Returns a list of all registered routes.
        The routes are tuples with 3 values (route:str, verb:str, action:func)
        """

        return self._actions

    def register_actions(self, prefix_routes):
        """
        Register actions in the controller in the controller directory.

        :Parameters:
        - `prefix_routes`: Tell the framework to prefix the route with the
        name of the controller.

        .. Notes:: `controllers` are defined in the controllers directory in
        the application's root directory. For instance, if the application has
        a controller named `userController.py` and for this controller there's
        a action defined with the route /get/{id:int}, if `init_route` is
        called with the parameter `prefix_route` set to `True`, the action will
        be registered as /user/get/{id:int}
        """

        modules = self._import_modules()
        # Get a list of the controller that have been successfully imported.
        controllers = [getattr(modules, ctrl) for ctrl in dir(modules)
                       if re.match(self._recontroller, ctrl)]

        if len(controllers) <= 0:
            print('Any controller has been registered.')
            return

        for controller in controllers:
            # First all dunder functions and properties are excluded
            controller_functions = [getattr(controller, func)
                                    for func in dir(controller)
                                    if not func.startswith('__')]

            # Get only tuples (actions defined in the controllers)
            actions = [action for action in controller_functions
                       if isinstance(action, tuple)]

            if prefix_routes:
                actions = self._prefix_routes(controller, actions)

            self._actions.extend(actions)

    def _prefix_routes(self, controller, actions):
        """
        Append the name of the controller (without the sufix 'Controller')
        to the route path.

        :Parameters:
        - `controller`: the controller object
        - `actions`: the actions that have been registered in the `controller`

        .. Note:: `actions` is a tuple (route, verb, func) where:
                  - `route`: the URI to the action
                  - `verb`: which HTTP verb the action will respond to
                  - `func`: the action function
        """

        prefixed = []

        for route, verb, func, additional_methods in actions:
            module, name = controller.__name__.split('.')
            name = name.replace('Controller', '')

            if not route.startswith('/'):
                route = f'/{route}'

            prefixed.append(
                (f'/{name}{route}', verb, func, additional_methods)
            )

        return prefixed

    def _import_modules(self):
        """
        Import all the content of the controllers directory and returns the
        module object.
        """

        self._controllers = self._get_controllers()
        modules = __import__('controllers',
                             globals(),
                             locals(),
                             self._controllers,
                             0)
        return modules

    def _get_controllers(self):
        """ Get a list of files in the controllers directory. """

        return [filename.replace('.py', '')
                for filename in os.listdir('controllers')
                if filename.endswith('Controller.py')]
