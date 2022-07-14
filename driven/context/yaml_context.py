#!/usr/bin/env python3

# BoBoBo


import os
from driven.app.db.sqlite3 import get_db
from driven.util import get_conf
from driven.util import get_logger


def build_context(conf_file):
    assert os.path.exists(conf_file)
    conf = get_conf(conf_file, 'topy_desk_servs')
    assert conf and 'log' in conf and 'db' in conf
    logger = get_logger(conf['log'])
    db = get_db(conf['db'])
    logger.info('topy-desk-servs init context with: %s' % conf)
    return dict(conf=conf, logger=logger, db=db)
