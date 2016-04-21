import re

class RouteResolver:

    def __init__(self, route_table):
        self._route_table = route_table

    def resolve(self, path):

        for route in self._route_table:
            m = re.compile(route)
            values = re.match(m, path)

            if values != None:
                print(values)
                (verb, action) = self._route_table[route]
                return (verb, action, values.groups())
