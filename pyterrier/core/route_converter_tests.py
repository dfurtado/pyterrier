from nose import with_setup
from nose.tools import raises
from .route_converter import RouteConverter


def test_registration_with_one_int_param():
    route = "/api/user/{id:int}"
    rc = RouteConverter()
    assert rc.convert(route) == "/api/user/([0-9]*)\/{0,1}$"

def test_registration_with_one_str_param():
    route = "/api/user/{name:str}"
    rc = RouteConverter()
    assert rc.convert(route) == "/api/user/(\w+)\/{0,1}$"

def test_registration_with_different_param_types():
    route = "/api/user/{id:int}/room/{room_name:str}"
    rc = RouteConverter()
    assert rc.convert(route) == "/api/user/([0-9]*)/room/(\w+)\/{0,1}$"

def test_registration_without_params():
    route = "/api/user/get"
    rc = RouteConverter()
    assert rc.convert(route) == "/api/user/get\/{0,1}$"

@raises(TypeError)
def test_registration_with_none_value():
    rc = RouteConverter()
    rc.convert()

@raises(TypeError)
def test_registration_with_empty_route():
    rc = RouteConverter()
    rc.convert("")

@raises(TypeError)
def test_registration_with_blank_spaces():
    rc = RouteConverter()
    rc.convert("      ")
