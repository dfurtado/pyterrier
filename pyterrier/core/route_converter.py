import re


class RouteConverter():
    """
    Helper class to convert the route URI into a regular expression that will
    later be used by the RouteResolver when searching the route table.
    """

    def __init__(self):

        self._rules = {
            "integer_params": (re.compile("\{\w+:int\}"), "([0-9]*)"),
            "str_param": (re.compile("\{\w+:str\}"), "(\w+)"),
        }

    def convert(self, route):
        """
        Convert the action URI to a regular expression.

        :Parameters:
        - `route`: the action URI
        """

        for key in self._rules:
            (m, n) = self._rules[key]
            route = m.sub(n, route)

        return "{route}{end}".format(route=route, end="/{0,1}$")
