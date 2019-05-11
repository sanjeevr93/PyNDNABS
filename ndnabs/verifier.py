# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/Mamietti/ABS

from . import ABS
from . import utils
from .sha256_with_abs_signature import Sha256WithAbsSignature

import pyndn
import base64

class Verifier():

    pk = None
    abs = None
    publicParams = None

    def __init__(self, db):
        self.db = db
        self.abs = ABS()
        try:
            self.pk = utils.deserialize(self.db.load('pk'), self.abs.group)
            self.publicParams = pyndn.Data()
            self.publicParams.wireDecode(base64.b64decode(self.db.load('publicParams')))
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

    def _verify(self, encodedSignature, message, attributes):
        signature = utils.deserialize(encodedSignature, self.abs.group)
        return self.abs.verify(self.pk, signature, message, attributes)

    def verify(self, wire):
        data = pyndn.Data()
        data.wireDecode(wire)
        signature = Sha256WithAbsSignature(data.getSignature())
        name = signature.getKeyLocator().getKeyName()
        attributes = name[-1].getValue().toBytes().split(b'&')

        print ("Data name: %s; KeyLocator: %s" % (data.getName().toUri(), signature.getKeyLocator().getKeyName().toUri()))
        print ("Verifying using: %s" % str(b' & '.join(attributes), 'utf-8'))

        return self._verify(signature.getSignature().toBytes(), data.wireEncode().toSignedBytes(), attributes)
