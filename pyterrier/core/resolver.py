import re

class RouteResolver:

    def __init__(self, route_table):
        self._route_table = route_table

    def resolve(requestinfo):
        (verb, path) = requestinfo;

        for route in self._route_table:
            m = re.compile(route)
            values = re.match(m, path)

            if values != None:
                return self._route_table[route]
