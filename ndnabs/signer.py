# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from . import ABS
from . import utils
from .sha256_with_abs_signature import Sha256WithAbsSignature

import pyndn
import base64

class Signer():
    pk = None
    ska = None
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
        try:
            self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)
        except:
            # print("SKA not available")
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

    def install_secret(self, encodedSka):
        self.db.save('ska', encodedSka)
        self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)

    def get_secret(self):
        '''Get the installed secret key'''
        return self.db.load('ska')

    def get_attributes(self):
        '''Get attributes associated with the installed secret key'''
        return self.ska['attributes']

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
            if not isinstance(self.publicParams, pyndn.Data):
                raise RuntimeError("Public parameters must be installed before signing")
            locator.append(self.publicParams.getName())

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
