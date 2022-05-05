#!/usr/bin/env python3

# BoBoBo


from driven.embed.context.server_conf import get_filter_algorithm_module
from driven.filter.common_filter_headers import filter_cons
import importlib


def filter_in(request, fr, logger):
    cookies = request['HTTP_COOKIE']
    if filter_cons.CLIENT_FILTER_HEADER in cookies:
        client_info = cookies[filter_cons.CLIENT_FILTER_HEADER].value
    else:
        logger.info('No cookie of: %s' % filter_cons.CLIENT_FILTER_HEADER)
        return False

    if not client_info:
        print('DANGER: Unauthorized client %s' % str(client_info))
        return False

    try:
        algorithm = importlib.import_module(get_filter_algorithm_module(fr))
        algorithm = importlib.reload(algorithm)
    except Exception as ex:
        print('Failed to get client filter algorithm: %s' % ex)
        return False

    try:
        request[filter_cons.ENVIRON_CLIENT_HEADER] = algorithm.calc(
            client_info)
    except Exception as ex:
        print('DANGER: Illegal client for: %s' % ex)
        return False
    else:
        return True


def filter_out(response, fr, logger):
    pass
