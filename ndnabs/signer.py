# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/Mamietti/ABS

from . import ABS
from . import utils
from .verifier import Verifier
from .sha256_with_abs_signature import Sha256WithAbsSignature

import pyndn
import base64

class Signer(Verifier):
    ska = None

    def __init__(self, db):
        super(Signer, self).__init__(db)

        try:
            self.ska = utils.deserialize(self.db.load('ska'), self.abs.group)
        except:
            # print("SKA not available")
            pass

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
