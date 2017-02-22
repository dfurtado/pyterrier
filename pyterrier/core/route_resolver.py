import re

class RouteResolver:
    """
    Lookup the request route in the route table.
    """

    def __init__(self, route_table):
        self._route_table = route_table


    def resolve(self, path):
        """
        Search the route table by the request route.
        If found it will return a tuple containing the HTTP verb, the action
        to be executed and also a list of parameter values sent as part of the
        route URL.
        """

        for route in self._route_table:
            m = re.compile(route)
            values = re.match(m, path)

            if values != None:
                (verb, action) = self._route_table[route]
                return (verb, action, values.groups())
