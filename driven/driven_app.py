#!/usr/bin/env python3

# BoBoBo

import importlib

import driven.util as util
from driven.app.app_context import wrap_context
from driven.app.app_headers import header_const
from driven.app.app_response import response_404
from driven.app.app_response import response_500
from driven.app.app_response import response_json
from driven.app.app_response import response_raw


def driven_app(app_name, app_context):

    app_context = wrap_context(app_name, app_context)

    def app(environ, start_response):
        nonlocal app_context

        try:
            response = dispatch(environ, app_context)
        except Exception as ex:
            app_context.error(
                'failed to dispatch environ: %s' % str(environ), ex)
            response = response_500()

        if start_response:
            app_context.debug('app response: %s' % str(response))
            start_response(response['status'], response['headers'])
            if response['content']:
                return [(response['content']).encode('utf-8')]
            else:
                return []
        else:
            return response

    return app


def dispatch(environ, app_context):
    path = environ['PATH_INFO']
    action = get_action(path, app_context)
    if not action:
        return response_404()

    method = environ['REQUEST_METHOD']
    auth = environ.get(header_const.ENVIRON_AUTH_HEADER, None)
    client = environ.get(header_const.ENVIRON_CLIENT_HEADER, None)
    auth = {'auth': auth, 'client': client}

    # Hope server parsed parameters as json
    parameters = environ.get(header_const.ENVIRON_PARSED_PARAMETERS, None)
    # If not parse it
    if not parameters:
        parameters = util.parse_environ_parameters(method, environ)

    if parameters:
        app_context.debug(
            'dispatch parameters: %s' % str(parameters))
        if isinstance(parameters, dict):
            return action(app_context, auth, **parameters)
        else:
            return action(app_context, auth, parameters)
    else:
        return action(app_context, auth)


def get_action(path, app_context):
    """Deside what to execute."""
    assert path
    mm = path.split('/')
    assert len(mm) > 0
    mm = mm[1:]

    """
    check the top of package name must be one of apps.
    """
    app_name = mm[0]
    if not (app_name == app_context.get_app_name()):
        app_context.error(
            'failed to load action with path: %s for error app_name' % path)
        return None

    """
    the name of function called is same with module.
    """
    try:
        function_name = mm[-1]
        module_name = '.'.join(mm)
        m = importlib.import_module(module_name)
        func = getattr(m, function_name)
    except Exception as ex:
        app_context.error(
            'failed to load action with path: %s' % path, ex)
        return None

    return wrap_action_response(func) if func else None


def wrap_action_response(func):

    def wrapper(*args, **kw):
        result = func(*args, **kw)
        if isinstance(result, tuple):
            # multi returned value with the headers as the second value
            res = result[0]
            headers = result[1]
            if isinstance(res, dict) or isinstance(res, list):
                return response_json(res, headers)
            else:
                return response_raw(res, headers)
        elif isinstance(result, dict) or isinstance(result, list):
            return response_json(result)
        else:
            return response_raw(result)

    return wrapper
