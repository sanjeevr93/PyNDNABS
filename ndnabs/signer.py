# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from . import ABS
from . import utils

class Signer():

    def __init__(self, db):
        self.db = db
        self.abs = ABS()
        try:
            self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)
        except:
            pass
        try:
            self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)
        except:
            pass

    def install_public_parameters(self, encodedPk):
        self.db.save('pk', encodedPk)
        self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)
        
    def install_secret(self, encodedSka):
        self.db.save('ska', encodedSka)
        self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)

    def get_secret(self): # this is returning secret keys!!!
        return self.db.load('ska')

    def sign(self, message, attributes):
        signature = self.abs.sign(self.pk, self.ska, message, attributes)
        return utils.serialize(signature, self.abs.group)
