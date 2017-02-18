import os, glob, re

class RouteDiscovery:


    def __init__(self):
        self._actions = []
        self.llers = []
        self._controller_folder = "controllers"
        self._recontroller = re.compile(r"[\w\-]+(Controller)$")


    @property
    def actions(self):
        """
        Returns a list of all registered routes.
        The routes are tuples with 3 values (route:str, verb:str, action:func)
        """

        return self._actions


    def register_actions(self, prefix_routes):
        """
        Import all the contents of the folder "controllers" and a list of
        tuples representing every route that will be available.
        The tuple contains the route, the HTTP verb and the function that will be
        executed when a request is done to the route.
        """

        modules = self._import_modules()
        # Get a list of the controller that have been successfully imported.
        controllers = [getattr(modules, ctrl) for ctrl in dir(modules) if re.match(self._recontroller, ctrl)]

        if len(controllers) <= 0:
            print("Any controller has been registered.")
            return

        for controller in controllers:
            # First all dunder functions and properties are excluded
            controller_functions = [getattr(controller, func) for func in dir(controller) if not func.startswith("__")]

            # Get only tuples (actions defined in the controllers)
            actions = [action for action in controller_functions if isinstance(action, tuple)]

            if prefix_routes:
                actions = self._prefix_routes(controller, actions)

            self._actions.extend(actions)


    def _prefix_routes(self, controller, actions):
        """
        Append the name of the controller (without the sufix) to the route path.
        """

        prefixed = []

        for route, verb, func in actions:
            module, name = controller.__name__.split(".")
            name = name.replace("Controller", "")
            prefixed.append((f"/{name}{route}", verb, func))

        return prefixed


    def _import_modules(self):
        """
        Import all the content of the "controllers" folder and returns the
        module object.
        """

        self._controllers = self._get_controllers()
        modules = __import__('controllers', globals(), locals(), self._controllers, 0)
        return modules


    def _get_controllers(self):
        """
        Get a list of files in the "controllers" folder.
        """

        ctrl_dir = os.path.join(os.curdir, "controllers", "*Controller.py")
        file_list = glob.glob(ctrl_dir)
        return [x.replace(".py", "").split("/")[2] for x in file_list]
