# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

import pickledb
import base64

class Db:
    def save(self, key, value):
        raise RuntimeError("Use specific database instance")

    def load(self, key, value):
        raise RuntimeError("Use specific database instance")
        

class PickleDb:
    def __init__(self, path):
        self.db = pickledb.load(path, True)

    def save(self, key, value):
        self.db.set(key, str(base64.b64encode(value), 'ascii'))

    def load(self, key):
        value = base64.b64decode(self.db.get(key).encode('ascii'))
        if not value:
            raise KeyError("'%s' does not exist in the database" % key)
        return value
