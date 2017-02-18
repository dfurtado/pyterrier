import re

class RouteConverter():

    def __init__(self):

        self._rules = {
            "integer_params": (re.compile("\{\w+:int\}"), "([0-9]*)"),
            "str_param":      (re.compile("\{\w+:str\}"), "(\w+)"),
         }

    def convert(self, route):

        for key in self._rules:
            (m,n) = self._rules[key]
            route = m.sub(n, route)

        return "{route}{end}".format(route = route, end = "/{0,1}$")


