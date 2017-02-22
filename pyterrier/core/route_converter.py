import re

class RouteConverter():
    """
    Helper class to convert the route URL into a regular expression that will
    later be used by the RouteResolver to lookup the route table.
    """


    def __init__(self):

        self._rules = {
            "integer_params": (re.compile("\{\w+:int\}"), "([0-9]*)"),
            "str_param":      (re.compile("\{\w+:str\}"), "(\w+)"),
         }

    def convert(self, route):
        """
        Get a route value and convert it to a regular expression.
        """

        for key in self._rules:
            (m,n) = self._rules[key]
            route = m.sub(n, route)

        return "{route}{end}".format(route = route, end = "/{0,1}$")


