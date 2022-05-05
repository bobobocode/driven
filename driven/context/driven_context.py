#!/usr/bin/env python3

# BoBoBo

import importlib
from collections import UserDict
import driven.util as util
from driven.driven_app import driven_app
import driven.context.driven_conf as driven_conf
import driven.app.app_context as app_context


class DrivenContext(UserDict):

    def init_by_conf_file(self, conf_file):
        self.clear()

        print('init driven context with: %s' % conf_file)
        conf = driven_conf.get_conf(conf_file)
        self.logger = util.get_logger(conf.get('log', {}))

        self.init_apps(conf)

        driven_ctx = DrivenContext()
        driven_ctx.set_logger(self.logger)
        driven_ctx.set_conf(conf)
        self.update(driven_ctx)

    def init_apps(self, conf):
        apps = {}
        self.clear_app_pythonpath()
        for app_name in driven_conf.get_apps(conf):
            app_deploy = driven_conf.get_app_deploy(conf, app_name)
            self.add_app_pythonpath(app_deploy)

            app_ctx = self.init_app_context(app_name, conf)
            apps[app_name] = driven_app(app_name, app_ctx)
            self.set_app_context(app_name, app_ctx)

        self.set_apps(apps)

    def init_app_context(self, app_name, conf):

        def _build(build_context_module_name, app_conf_file):
            try:
                m = importlib.import_module(build_context_module_name)
                importlib.reload(m)  # For reload new code.
                return m.build_context(app_conf_file)
            except Exception as ex:
                self.logger.error(
                    'failed to execute context builder for app[ % s]' % app_name,
                    exc_info=True)
                raise ex

        build_context_module_name = driven_conf.get_app_context_builder(
            conf, app_name)
        app_conf_file = driven_conf.get_app_conf_file(conf, app_name)
        ctx = _build(build_context_module_name, app_conf_file)
        ctx = app_context.wrap_context(app_name, ctx)
        self.logger.info(
            'init app[%s] context with conf [%s]' % (app_name, app_conf_file))
        return ctx

    def add_app_pythonpath(self, path):
        util.add_pythonpath(path)
        self.logger.info('add python path: %s' % path)
        k = '_app_pythonpathes_'
        if k not in self:
            self[k] = []
        self[k].append(path)

    def clear_app_pythonpath(self):
        k = '_app_pythonpathes_'
        if k in self:
            for p in self[k]:
                util.remove_pythonpath(p)

    def set_app_context(self, app_name, ctx):
        assert app_name
        key = '_driven_apps_context_'
        if key not in self:
            self[key] = {}
        self[key][app_name] = ctx

    def get_app_context(self, app_name):
        return self['_driven_app_context_'][app_name]

    def get_logger(self):
        return self.get('_driven_logger_', None)

    def get_conf(self):
        return self.get('_driven_conf_', None)

    def get_apps(self):
        return self.get('_driven_apps_', None)

    def set_logger(self, val):
        self['_driven_logger_'] = val

    def set_conf(self, val):
        self['_driven_conf_'] = val

    def set_apps(self, val):
        self['_driven_apps_'] = val
