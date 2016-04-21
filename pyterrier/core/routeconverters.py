import re

class DefaultRouteConverter():

    def __init__(self):

        self._rules = {
            "integer_params": (re.compile("\{\w+:int\}"), "(?P<intvalue>[0-9]*)"),
            "str_param":      (re.compile("\{\w+:str\}"), "(?P<strvalue>\w+)"),
         }

    def convert(self, route):

        for key in self._rules:
            (m,n) = self._rules[key]
            route = m.sub(n, route)

        return route


