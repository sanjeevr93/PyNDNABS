# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from .abs import ABS
from . import utils

class AttributeAuthority:

    def __init__(self, db):
        self.abs = ABS()
        self.db = db
        try:
            self._load()
        except:
            self._setup()

    def _setup(self):
        self.apk, self.ask = self.abs.authSetup()
        
        self.db.save('apk', utils.serialize(self.apk, self.abs.group))
        self.db.save('ask', utils.serialize(self.ask, self.abs.group))

    def _load(self):
        self.apk = utils.deserialize(self.db.load('apk'), self.abs.group)
        self.ask = utils.deserialize(self.db.load('ask'), self.abs.group)

    def get_apk(self):
        return self.db.load('apk')
        
    def gen_attr_keys(self, attributes, serializedExistingSka = None):
        Kbase = None
        existingSka = None
        if serializedExistingSka:
            existingSka = utils.deserialize(serializedExistingSka, self.abs.group)
            Kbase = existingSka['Kbase']

        ska = self.abs.generateattributes(self.ask, attributes, Kbase)

        if existingSka:
            ska = {**existingSka, **ska}
        
        return utils.serialize(ska, self.abs.group)
