#!/usr/bin/env python3

# BoBoBo

import os
import asyncio
import json
import uuid
import stat
import traceback
from multiprocessing import Process
from multiprocessing import Queue

import driven.context.driven_context as driven_context
import driven.context.driven_conf as driven_conf
from driven.app.app_headers import header_const
import driven.app.app_response as app_response
import driven.util as util


class DrivenProcess(Process):

    driven_queue = None
    driven_processes = []

    def __init__(self, process_name, conf_file):
        Process.__init__(self)
        self.name = process_name
        self.init_context(conf_file)

        self.eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.eventloop)
        self.info('inited eventloop')
        if DrivenProcess.driven_queue is None:
            DrivenProcess.driven_queue = Queue()
            self.info('created driven queue')

    def info(self, msg):
        self.logger.info(('driven-process[%s] ' % self.name) + msg)

    def debug(self, msg):
        self.logger.debug(('driven-process[%s] ' % self.name) + msg)

    def error(self, msg, ex):
        if ex:
            self.logger.error(
                ('driven-process[%s] ' % self.name) + msg, exc_info=True)
        else:
            self.logger.error(
                ('driven-process[%s] ' % self.name) + msg)

    def init_context(self, conf_file):
        context = driven_context.DrivenContext()
        context.init_by_conf_file(conf_file)
        self.context = context
        self.logger = context.get_logger()
        self.info('init context: %s' % self.context)

    def run(self):
        self.driven_pid = os.getpid()
        self.info('running in pid[%s]' % os.getpid())

        async def async_do_request(queue_request):
            self.process_queue_request(queue_request)

        self.info("ready to do request")
        while True:
            queue_request = None
            try:
                queue_request = DrivenProcess.driven_queue.get(block=True)
            except Exception as ex:
                self.error("get request timeout from driven queue", ex)
            if queue_request:
                self.debug("received queue request: %s" % str(queue_request))
                coroutine = async_do_request(queue_request)
                self.eventloop.run_until_complete(coroutine)

    def process_request(self, driven_request):
        '''
        do request without subprocess
        '''
        path = driven_request['PATH_INFO']
        try:
            app_name = path.split('/')[1]
            if app_name in self.context.get_apps():
                res = self.context.get_apps()[app_name](driven_request, None)
            else:
                res = app_response.response_404()
        except Exception as ex:
            self.error('failed to do request: %s' % str(driven_request), ex)
            return app_response.response_500()
        else:
            return res

    def process_queue_request(self, queue_request):
        res = self.process_request(queue_request[0])
        if not res:
            res = app_response.response_500()

        response_fd = os.open(
            queue_request[1], os.O_SYNC | os.O_CREAT | os.O_RDWR)
        response_str = json.dumps(res) + '\r\n'
        os.write(response_fd, response_str.encode('utf-8'))
        self.debug('write named pipe[%s] content: %s' %
                   (queue_request[1], response_str))
        os.close(response_fd)


def driven_process_wsgi_request(wsgi_request, response_named_pipe):
    driven_request = convert_driven_request(wsgi_request)
    queue_request = (driven_request, response_named_pipe)
    DrivenProcess.driven_queue.put(queue_request)


def convert_driven_request(wsgi_request):
    # TODO convert wsgi request to driven request
    if wsgi_request:
        method = wsgi_request['REQUEST_METHOD']
        parameters = util.parse_environ_parameters(method,
                                                   wsgi_request)
        wsgi_request[header_const.ENVIRON_PARSED_PARAMETERS] = parameters
        del wsgi_request['wsgi.input']
        del wsgi_request['HTTP_COOKIE']
        return wsgi_request
    else:
        return None


def apply_response_pipe():
    pipe_file = '/tmp/' + str(uuid.uuid1())
    fd = None
    try:
        os.mkfifo(pipe_file)
        # fd = os.open(pipe_file, flags=os.O_CREAT, mode=stat.S_IWGRP |
        #             stat.S_IRGRP | stat.S_IWUSR | stat.S_IRUSR | stat.S_IROTH)
    except Exception as ex:
        print("failed to create named pipe[%s] for: %s" % (pipe_file, ex))
        traceback.print_exc()
        raise ex
    else:
        return pipe_file


def start(process_name, process_conf_file):
    conf = driven_conf.get_conf(process_conf_file)
    mode = driven_conf.get_mode(conf)
    if 'process_local' == mode:
        # Maybe this mode is useless now
        global sync_driven_processor
        print('will run driven in local process')
        sync_driven_processor = DrivenProcess(process_name, process_conf_file)
        return sync_driven_processor
    elif 'process_new' == mode:
        print('pid[%s] starting driven-process[%s] ...' %
              (os.getpid(), process_name))
        driven_process = DrivenProcess(process_name, process_conf_file)
        driven_process.start()
        DrivenProcess.driven_processes.append(
            {'name': process_name, 'process': driven_process})
        return DrivenProcess.driven_processes
    else:
        print("invalid driven process mode: %s" % mode)
        return None
