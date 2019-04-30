# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from . import ABS
from . import utils

class Verifier:

    def __init__(self, db):
        self.db = db
        self.abs = ABS()
        try:
            self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)
        except:
            pass

    def install_public_parameters(self, encodedPk):
        self.db.save('pk', encodedPk)
        self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)

    def verify(self, encodedSignature, message, attributes):
        signature = utils.deserialize(encodedSignature, self.abs.group)
        return self.abs.verify(self.pk, signature, message, attributes)
