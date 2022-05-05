#!/usr/bin/env python

# BoBoBo

def mock_config(state):

    def conf(section, key, default):
        k = section + '.' + key if section else key
        return state[k] if k in state else default

    return conf
