#!/usr/bin/env python3

# BoBoBo

from collections import UserDict

import driven.util as util


def wrap_context(app_name, ctx):
    app_ctx = AppContext(ctx)
    app_ctx.set_app_name(app_name)

    logger = ctx.get('logger', None)
    if logger is None:
        logger = util.get_logger({'name': 'driven-app'})
    app_ctx.set_driven_logger(logger)

    return app_ctx


class AppContext(UserDict):

    def set_app_name(self, app_name):
        self['_app_name_'] = app_name

    def get_app_name(self):
        return self.get('_app_name_', 'default_app_name')

    def set_driven_logger(self, logger):
        self['_driven_logger_'] = logger

    def get_driven_logger(self):
        return self.get('_driven_logger_', None)

    def error(self, msg, ex=None):
        if ex:
            self.get_driven_logger().error(
                'driven-app[%s] ' % self.get_app_name() + msg, exc_info=True)
        else:
            self.get_driven_logger().error(
                'driven-app[%s] ' % self.get_app_name() + msg)

    def debug(self, msg):
        self.get_driven_logger().debug(
            'driven-app[%s] ' % self.get_app_name() + msg)
