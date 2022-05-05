#!/usr/bin/env python3

#BoBoBo#

import driven.app.db.database as database

import pymysql


def get_db(conf):
    return database.get_db(conf, pymysql)
