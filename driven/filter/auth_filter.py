#!/usr/bin/env python3

# BoBoBo

import driven.app.db.inside_cache as store
from driven.filter.common_filter_headers import filter_cons


def filter_in(request, fr, logger):
    cookies = request['HTTP_COOKIE']
    if filter_cons.AUTH_FILTER_HEADER in cookies:
        auth = store.get(cookies[filter_cons.AUTH_FILTER_HEADER].value)
        request[filter_cons.ENVIRON_AUTH_HEADER] = auth
        return True
    else:
        logger.info('No cookie of: %s' % filter_cons.AUTH_FILTER_HEADER)
        request[filter_cons.ENVIRON_AUTH_HEADER] = None
        return False


def filter_out(response, fr, logger):
    pass
