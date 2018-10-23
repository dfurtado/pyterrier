import cgi
import json
import mimetypes
import os
import re
import sys

from urllib.parse import urlparse

from typing import Any
from typing import Tuple
from typing import Optional
from typing import Dict

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

from pyterrier.core.request import Request
from pyterrier.core.route_resolver import RouteResolver
from pyterrier.encoders.default_json_encoder import DefaultJsonEncoder
from .view_result import ViewResult


class HttpRequestHandler(BaseHTTPRequestHandler):
    """ Le framework's HTTP handler. """

    def __init__(self,
                 route_table: Dict[str, Tuple[str, Any]],
                 config: Dict[str, str],
                 renderer, *args: Any) -> None:
        """
        Create a new request handler.
        :param route_table: A dict with route information, the key is the route
        as string and the value is a tuple containing the http verb and the
        action to be executed when the route is requested.
        """

        self._route_table = route_table
        self._resolver = RouteResolver(route_table)
        self._config = config
        self._renderer = renderer

        self._static_regex = re.compile(r'[/\w\-\.\_]+(?P<ext>\.\w{,4})$',
                                        re.IGNORECASE | re.DOTALL)

        BaseHTTPRequestHandler.__init__(self, *args)

        mimetypes.init()

    def _send_response(self,
                       results: Any, http_status: int,
                       content_type: Optional[str]='text/html'):
        """ Prepare response to be sent to the client """

        self.send_response(http_status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        if results:
            self.wfile.write(bytes(results, 'utf-8'))

    def _decode_results(self, data: Any):
        """ Decode the binary strings to utf-8 """

        return {x[0].decode('utf-8'): x[1][0].decode('utf-8')
                for x in data.items()}

    def do_DELETE(self) -> None:
        self.do_POST()

    def do_PUT(self) -> None:
        self.do_POST()

    def do_PATCH(self) -> None:
        self.do_POST()

    def do_POST(self) -> None:
        """ Handler POST requests """
        request = Request(self)

        try:
            action_info = self._resolver.resolve(self.path, request.method)
        except KeyError:
            return self._send_response({}, HTTPStatus.METHOD_NOT_ALLOWED)

        ctype, pdict = cgi.parse_header(self.headers.get_content_type())

        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('Content-Length'))
            postvars = cgi.parse_qs(self.rfile.read(length),
                                    keep_blank_values=1)
        else:
            postvars = {}

        if action_info:
            verb, handler, params = action_info
            decoded_str = self._decode_results(postvars)
            results = handler(decoded_str) if decoded_str else handler()
            response = self._prepare_json_result(results)
            self._send_response(*response)

    def do_GET(self) -> None:
        """
        Handle all post requests.
        It will get a request path and search for it in the route table.
        If the action for the request is found it will be executed and the
        response will be returned.
        """

        request = Request(self)

        if self.is_requesting_file(request.path):
            self._serve_file(request.path)

        try:
            action_info = self._resolver.resolve(request.path, request.method)
        except KeyError:
            return self._send_response({}, HTTPStatus.METHOD_NOT_ALLOWED)
        else:
            if not action_info:
                self._send_response({}, HTTPStatus.NOT_FOUND)
                return

        (verb, handler, params) = action_info
        handler.__self__.request = request
        results = handler(*params)

        response = None

        if isinstance(results, ViewResult):
            response = self._prepare_view_result(results)
        else:
            response = self._prepare_json_result(results)

        self._send_response(*response)

    def _prepare_view_result(self, view_result) -> Tuple[str, HTTPStatus, str]:
        """
        Render the view result returning the rendered view using the default
        template engine.

        view_result: It is an instance of ViewResult. See ViewResult in
        PyTerrier.http_handler for more details.
        """

        response: Tuple[str, HTTPStatus, str]

        try:
            result = self._renderer.render(view_result.template,
                                           view_result.context)
            response = (
                    result,
                    HTTPStatus.OK,
                    'text/html',
                    )
        except Exception as e:
            response = (
                    str(e),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    'application/json',
                    )

        return response

    def _prepare_json_result(self, json_result) -> Tuple[str, HTTPStatus, str]:
        """
        Parse the json result returning a prepare response to be sent
        to the client.
        The response will be a tuple containing:
        (HTTPStatus, data, content-type)

        json_result: It is a instance of HttpResult. See
        PyTerrier.http.http_result for more details.
        """

        response: Tuple[str, HTTPStatus, str]

        try:
            response = (
                    json.dumps(json_result.data, cls=DefaultJsonEncoder),
                    json_result.http_status,
                    'application/json',
                    )

        except TypeError as e:
            response = (
                    str(e),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    'application/json',
                    )

        return response

    def is_requesting_file(self, path):
        """
        Returns True if the it is requesting a file, otherwise, return False.

        path: The relative path to the static file. By default it will
        search in the static folder in the application root.
        """

        match = self._static_regex.search(path)

        return match is not None and match.group('ext') is not None

    def get_mime_type(self, path: str):
        """
        Returns the mime type base on the extension of the file that the
        client is requesting.

        path: The relative path to the static file. By default it will
        search in the static folder in the application root.
        """

        match = self._static_regex.search(path)

        if match and match.group('ext'):
            return mimetypes.types_map[match.group('ext')]

    def _serve_file(self, path: str):
        """
        Server a static file to the client.

        path: The relative path to the static file. By default it will
        search in the static folder in the application root.
        """

        parsed_req_url = urlparse(path)
        path = parsed_req_url.path

        path = os.path.normpath(self._config['staticfiles'] + path)

        try:
            mime_type = self.get_mime_type(path)
        except KeyError:
            self._send_response('Unsupported media type.',
                                HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            return

        if not os.path.exists(path):
            self._send_response('File not found.', HTTPStatus.NOT_FOUND)
        else:
            try:
                with open(path, encoding='utf-8') as f:
                    results = f.read()
                    self._send_response(results, HTTPStatus.OK, mime_type)
            except Exception:
                self._send_response(f'Internal Error {sys.exc_info()[0]}',
                                    HTTPStatus.INTERNAL_SERVER_ERROR)
                raise
