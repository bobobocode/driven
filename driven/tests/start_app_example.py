#!/usr/bin/env python3

# BoBoBo

import driven.util as util
import driven.embed.sengine.sengine as wsgi_server
import driven.driven_process as driven_process
from driven.driven_app import driven_app


if __name__ == "__main__":
    args = util.get_server_cmdargs()
    if args.mode == 'driven':
        driven_processes = driven_process.start(
            'driven-test-process', './driven-process-test.yaml')
        wsgi_server.bootstrap_with_driven(
            '', 8000, driven_process, {'name': 'sengine'})
    else:
        app = driven_app(
            'app_example', {'logger': util.get_logger({'name': 'app_example'})})
        wsgi_server.bootstrap(
            '', 8000, {'app_example': app}, {'name': 'sengine'})
