#!/usr/bin/env python

# BoBoBo

import os
import sqlite3
import json
import driven.db.database as database


class DB:

    def __init__(self, state):
        self.state = state

    def __call__(self):
        return self

    def __enter__(self):
        print("enter db")

    def __exit__(self, *args, **argv):
        print("exit db")


def sqlite3_db():
    return sqlite3.connect(db_path)


def mock_db(ctx):
    if 'script' in ctx:
        if 'sqlite3' == ctx['type']:
            db_path = ctx['locate']
            if os.system('./' + ctx['script'] + ' -p ' + db_path) != 0:
                print('Failed to execute mock db script: %s' % db_path)
                return None

            def sqlite3_db():
                nonlocal db_path
                return sqlite3.connect(db_path)
            return sqlite3_db

    elif 'state' in ctx:
        state = ctx['state']
        state_map = dict(map(lambda e:
                             tuple(map(lambda m: "".join(
                                 m.split()), e.split('=>'))),
                             state))
        print("db state:")
        print(str(state_map))

        database.query = mock_query(state_map)
        database.update = mock_update(state_map)
        database.insert = mock_insert(state_map)
        return DB(state)
    else:
        print('Failed to mock db.')
        return None


def mock_insert(state_map):
    def insert(conn, sqls, auto_close=True):
        nonlocal state_map
        print("Insert:")
        print(str(sqls))
        print("Total: %s", len(sqls))
    return insert


def mock_update(state_map):
    def update(conn, sql, param, auto_close=True):
        nonlocal state_map
        print(state_map[sql])
    return update


def mock_query(state_map):
    def query(conn, sql, param, auto_close=True):
        nonlocal state_map
        param_len = len(param)
        cuts = sql.split('?')
        placeholder_num = len(cuts) - 1
        add_placeholder_num = param_len - placeholder_num
        new_sql = ''
        if placeholder_num > 0:
            for i in range(len(cuts)):
                if i == len(cuts) - 1:
                    new_sql = new_sql + cuts[i]
                else:
                    new_sql = new_sql + cuts[i] + '?'
                    if i == 0:
                        for j in range(add_placeholder_num):
                            new_sql = new_sql + ',?'

        for p in param:
            new_sql = new_sql.replace('?', str(p), 1)

        sql = new_sql
        print("query sql: %s" % sql)
        k = "".join(sql.split())
        print(str(state_map))
        return json.loads(state_map[k])
    return query
