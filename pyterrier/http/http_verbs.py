from typing import Callable
from typing import List


def get(route: str, additional_methods: List[str]=[]) -> Callable:
    """
    States that a function will be executed when a GET request
    is sent to the server.

    .. Usages::

    To create a simple route without any parameters:

    @get('/')
    def main(self):
        pass

    In the example above the @get decorator states that the function will
    respond to a HTTP GET request and the return of this function will be the
    contents of a HTML template, in this case main.html

    The @get decorator also accepts variable parameters in the route URL. This
    can be achieved using placeholders. For example:

    @get('/user/{id:int}')
    def get(self, id):
        pass

    In this case when the client send a HTTP GET request to /users/1, the
    function get_user will be executed and the id integer parameter will
    be passed to it.

    The format for the placeholders are {name:type} where type
    can be: str or int.

    """

    return lambda func: (route, 'GET', func, additional_methods)


def post(route: str, additional_methods: List[str]=[]) -> Callable:
    """
    States that a function will be executed when a POST request
    is sent to the server.
    """

    return lambda func: (route, 'POST', func, additional_methods)


def put(route: str, additional_methods: List[str]=[]) -> Callable:
    """
    States that a function will be executed when a PUT request
    is sent to the server.
    """

    return lambda func: (route, 'PUT', func, additional_methods)


def patch(route: str, additional_methods: List[str]=[]) -> Callable:
    """
    States that a function will be executed when a PATCH request
    is sent to the server.
    """

    return lambda func: (route, 'PATCH', func, additional_methods)


def delete(route: str, additional_methods: List[str]=[]) -> Callable:
    """
    States that a function will be executed when a DELETE request
    is sent to the server.
    """

    return lambda func: (route, 'DELETE', func, additional_methods)
