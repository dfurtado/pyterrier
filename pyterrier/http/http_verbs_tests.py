from .http_verbs import get
from .http_verbs import post
from .http_verbs import put
from .http_verbs import patch
from .http_verbs import delete


def function_mock():
    return 'test'


def decorator_without_addition_http_methods(
        decorator,
        route,
        method=function_mock,
        additional_methods=[]):

    decorator_func = decorator(route, additional_methods)

    _route, _method, _action, _additional_methods = decorator_func(
        function_mock
    )

    assert _route == route

    assert _method == method

    assert callable(_action)
    assert _action() == 'test'

    assert isinstance(additional_methods, list)

    if additional_methods:
        results = [item in additional_methods for item in _additional_methods]
        assert False not in results


def test_get_without_addition_methods():
    decorator_without_addition_http_methods(get, '/api/test/get', 'GET')


def test_get_with_additional_methods():
    decorator_without_addition_http_methods(
        get,
        '/api/test/get',
        'GET',
        additional_methods=['POST']
    )


def test_post_without_addition_methods():
    decorator_without_addition_http_methods(post, '/api/test/post', 'POST')


def test_post_with_additional_methods():
    decorator_without_addition_http_methods(
        post,
        '/api/test/post',
        'POST',
        additional_methods=['PUT']
    )


def test_put_without_addition_methods():
    decorator_without_addition_http_methods(put, '/api/test/put', 'PUT')


def test_put_with_additional_methods():
    decorator_without_addition_http_methods(
        put,
        '/api/test/put',
        'PUT',
        additional_methods=['POST']
    )


def test_patch_without_addition_methods():
    decorator_without_addition_http_methods(patch, '/api/test/patch', 'PATCH')


def test_patch_with_additional_methods():
    decorator_without_addition_http_methods(
        patch,
        '/api/test/patch',
        'PATCH',
        additional_methods=['PUT']
    )


def test_delete_without_addition_methods():
    decorator_without_addition_http_methods(
        delete,
        '/api/test/delete',
        'DELETE'
    )


def test_delete_with_additional_methods():
    decorator_without_addition_http_methods(
        delete,
        '/api/test/delete',
        'DELETE',
        additional_methods=['POST']
    )
