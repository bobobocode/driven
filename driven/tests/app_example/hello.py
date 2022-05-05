#!/usr/bin/env python3

# BoBoBo


def hello(context, auth, name):
    if context:
        context['logger'].info('Hello %s!' % name)
    return 'Hello %s!' % name
