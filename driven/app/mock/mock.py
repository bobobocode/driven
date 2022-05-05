#!/usr/bin/env python

# BoBoBo

from driven.mock.mock_config import mock_config
from driven.mock.mock_kv import mock_kv
from driven.mock.mock_db import mock_db
from driven.mock.mock_logger import mock_logger
import yaml


def mock_context(context_file_name, top_key):
    try:
        with open(context_file_name, mode='r') as cf:
            ctx = yaml.load(cf, Loader=yaml.CLoader)[top_key]
    except Exception as ex:
        print('Failed to load test context file: ' + str(ex))
        return None

    return dict(zip(
        list(map(lambda k: ctx[k]['name'], list(ctx.keys()))),
        list(map(mock_ctx_obj(ctx), list(ctx.keys())))))


def mock_ctx_obj(ctx):
    def _mock_ctx_obj(k):
        nonlocal ctx
        print("mock [%s] ..." % k)
        f = {
            k == 'config': lambda k: mock_config(ctx[k]["state"]),
            k == 'db': lambda k: mock_db(ctx[k]),
            k == 'kv': lambda k: mock_kv(ctx[k]["state"]),
            k == 'logger': lambda k: mock_logger(ctx[k]["etc"])
        }[True]
        return f(k)

    return _mock_ctx_obj
