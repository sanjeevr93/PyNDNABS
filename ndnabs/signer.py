# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from . import ABS
from . import utils
from .sha256_with_abs_signature import Sha256WithAbsSignature

import pyndn
import base64

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

    def install_secret(self, encodedSka):
        self.db.save('ska', encodedSka)
        self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)

    def get_secret(self): # this is returning secret keys!!!
        return self.db.load('ska')

    def _sign(self, message, attributes):
        if not isinstance(message, bytes):
            raise RuntimeError("Can only sign bytes")
        signature = self.abs.sign(self.pk, self.ska, message, attributes)
        return utils.serialize(signature, self.abs.group)

    def sign(self, data, attributes, selfSign = False):
        if not isinstance(data, pyndn.Data):
            raise RuntimeError("ndnabs.Signer can only sign data packets")

        signatureInfo = Sha256WithAbsSignature()
        locator = pyndn.Name()
        if selfSign:
            locator.append(data.getName())
        else:
            pass
            # todo: set attribute authority name

        locator.append(b'&'.join(attributes))
        keyLocator = pyndn.KeyLocator()
        keyLocator.setType(pyndn.KeyLocatorType.KEYNAME)
        keyLocator.setKeyName(locator)
        data.setSignature(signatureInfo)
        data.getSignature().setKeyLocator(keyLocator)
        data.getSignature().wireEncode()

        toSign = data.wireEncode()

        signatureBytes = self._sign(toSign.toSignedBytes(), attributes)
        data.getSignature().setSignature(signatureBytes)

        data.wireEncode()
