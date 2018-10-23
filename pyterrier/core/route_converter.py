import re

from pyterrier.validators.str_validators import is_none_or_empty


class RouteConverter():
    """
    Helper class to convert the route URI into a regular expression that will
    later be used by the RouteResolver when searching the route table.
    """

    def __init__(self):

        self._rules = {
            'integer_params': (re.compile(r'{\w+:int}'), r'([0-9]*)'),
            'str_param': (re.compile(r'{\w+:str}'), r'(\\w+)'),
        }

        self._trailing_regex = r'/{0,1}$'

    def convert(self, route: str) -> str:
        """
        Convert the action URI to a regular expression.

        :Parameters:
        - `route`: the action URI
        """

        try:
            if is_none_or_empty(route):
                raise TypeError()

            if not route.startswith('/'):
                route = f'/{route}'

            for key in self._rules:
                (m, n) = self._rules[key]
                route = m.sub(n, route)

            return f'{route}{self._trailing_regex}'

        except (TypeError, AttributeError):
            message = ('The argument `route` is not a `str` or it does'
                       'not contain any value.')
            raise TypeError(message)
