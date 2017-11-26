import re
from typing import Tuple
from typing import Dict
from typing import Any
from typing import Callable


class RouteResolver:
    """
    Lookup the request route in the route table.
    """

    def __init__(self, route_table: Dict[str, Tuple[str, Any]]) -> None:
        self._route_table = route_table

    def resolve(self, uri: str, http_verb: str) -> Tuple[str, Callable, Tuple]:
        """
        Search the requested URI in the framework's route table.

        :Parameters:
        - `path`: the request URI

        ..Note:: If found it will return a tuple containing the HTTP verb, the
        action to be executed and also a list of parameter values sent as part
        of the route URL.
        """
        routes = self._route_table[http_verb]

        for route_definition in routes:
            route_def_uri, route_def_func = route_definition
            values = re.match(route_def_uri, uri)

            if values is not None:
                return (http_verb, route_def_func, values.groups())
