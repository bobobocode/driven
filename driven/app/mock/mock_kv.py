#!/usr/bin/env python

# BoBoBo

class KV:

    def __init__(self, state):
        self.state = state
        print("kv state:")
        print(str(state))

    def __enter__(self):
        return self

    def __exit__(self, *argv, **args):
        pass

    def __call__(self):
        print("kv mocker be called: %s" % str(self))
        return self

    def get(self, k):
        print("get with: %s" % k)
        return self.state[k]

    def set(self, k, v, **args):
        self.state[k] = v
        print('Set %s = %s' % (k, v))
        print('\tand with: ' + str(args))


def mock_kv(state):
    return KV(state)
