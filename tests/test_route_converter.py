import pytest

from pyterrier.core.route_converter import RouteConverter


def test_registration_with_one_int_param():
    route = '/api/user/{id:int}'
    rc = RouteConverter()
    assert rc.convert(route) == r'/api/user/([0-9]*)/{0,1}$'


def test_registration_with_one_str_param():
    route = '/api/user/{name:str}'
    rc = RouteConverter()
    assert rc.convert(route) == r'/api/user/(\w+)/{0,1}$'


def test_registration_with_different_param_types():
    route = '/api/user/{id:int}/room/{room_name:str}'
    rc = RouteConverter()
    assert rc.convert(route) == r'/api/user/([0-9]*)/room/(\w+)/{0,1}$'


def test_registration_without_params():
    route = '/api/user/get'
    rc = RouteConverter()
    assert rc.convert(route) == r'/api/user/get/{0,1}$'


def test_registration_without_slash_prefix():
    route = 'api/user/get'
    rc = RouteConverter()
    assert rc.convert(route) == r'/api/user/get/{0,1}$'


def test_registration_with_none_value():
    rc = RouteConverter()
    with pytest.raises(TypeError):
        rc.convert()


def test_registration_with_empty_route():
    rc = RouteConverter()
    with pytest.raises(TypeError):
        rc.convert('')


def test_registration_with_blank_spaces():
    rc = RouteConverter()

    with pytest.raises(TypeError):
        rc.convert('      ')


def test_registration_with_non_str_value():
    with pytest.raises(TypeError):
        RouteConverter(1)
