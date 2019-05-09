# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from . import ABS
from . import utils

import pyndn
import base64

class Signer(Object):
    pk = None
    abs = None
    publicParams = None

    def __init__(self, db):
        self.db = db
        self.abs = ABS()
        try:
            self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)
        except:
            # print("PK not available")
            pass

    def _install_pk(self, encodedPk):
        self.db.save('pk', encodedPk)
        self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)

    def install_public_params(self, publicParams):
        self.db.save('publicParams', publicParams)
        self.publicParams = pyndn.Data()
        self.publicParams.wireDecode(base64.b64decode(publicParams))

        # TODO: verify validity of public parameters

        encodedPk = self.publicParams.getContent().toBytes()
        self._install_pk(encodedPk)

    def get_public_params_info(self):
        return self.publicParams
