#!/usr/bin/env python3

#BoBoBo#

import redis


def get_db(conf):
    if not conf:
        return None

    conn_pool = None

    def _get_conn():
        nonlocal conf
        nonlocal conn_pool
        if conn_pool is None:
            conn_pool = redis.ConnectionPool(**conf)
        conn = redis.Redis(connection_pool=conn_pool,
                           decode_responses=True)
        return conn

    return _get_conn
