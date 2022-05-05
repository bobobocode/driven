#!/usr/bin/env python3

# BoBoBo

from argparse import ArgumentParser

import driven.context.driven_context as driven_context
import driven.driven_process as driven_process
import driven.embed.sengine.sengine as sengine_server
import driven.embed.tornado as tornado_server
import driven.embed.wsgi_server as wsgi_server


def execute_command(args):
    print('driven execute: %s' % args)
    command = args.command

    if 'sengine' == command:
        process_name, process_conf_path = args.process_config.split(':')
        driven_process.start(process_name, process_conf_path)
        sengine_server.bootstrap_with_driven(
            '', args.port, driven_process, {'name': 'sengine'})
    else:
        app_name, driven_process_conf_path = args.driven_app_config.split(':')
        context = driven_context.DrivenContext()
        context.init_by_conf_file(driven_process_conf_path)
        try:
            app = context.get_apps()[app_name]
        except Exception as ex:
            print('failed to build app[%s] with conf[%s] for %s' % (
                app_name, driven_process_conf_path, str(ex)))
            return 1
        if 'tornado' == command:
            tornado_server.bootstrap(args.port, app)
        elif 'wsgi' == command:
            wsgi_server.bootstrap('', args.port, app)
        else:
            print('driven command unknown')
            return 1


if __name__ == '__main__':
    parser = ArgumentParser()
    opt = parser.add_argument
    opt('-c', '--command', dest='command',
        help='Command to execute')
    opt('-p', '--port', dest='port', type=int,
        help='Port for command server', default=8080)
    opt('-s', '--process', dest='process_config',
        help='Driven process config')
    opt('-a', '--driven-app', dest='driven_app_config',
        help='Indicate one driven app')

    args = parser.parse_args()
    print('Run with parameters: %s' % args)

    res = execute_command(args)
    exit(res)
