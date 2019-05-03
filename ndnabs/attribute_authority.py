# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from .abs import ABS
from . import utils
from .signer import Signer

import pyndn
from datetime import datetime
import base64

class AttributeAuthority:

    def __init__(self, db):
        self.abs = ABS()
        self.db = db
        try:
            self._load()
        except:
            pass

    def setup(self, name):
        self.apk, self.ask = self.abs.authSetup()
        self.self_attributes = [b'self', name.toUri().encode('utf-8')]
        
        self.db.save('apk', utils.serialize(self.apk, self.abs.group))
        self.db.save('ask', utils.serialize(self.ask, self.abs.group))

        data = pyndn.Data(pyndn.Name(name).append("ABS").appendVersion(datetime.timestamp(datetime.now())))
        meta = pyndn.MetaInfo()
        meta.setType(pyndn.ContentType.KEY)
        meta.setFreshnessPeriod(86400*1000.0) # 1 day
        data.setMetaInfo(meta)
        data.setContent(self.db.load('apk'))

        signer = Signer(self.db)
        signer._install_pk(self.db.load('apk'))
        signer.install_secret(self.gen_attr_keys(self.self_attributes))
        signer.sign(data, self.self_attributes, selfSign = True)

        signer.install_public_params(base64.b64encode(data.wireEncode().toBytes()))

    def _load(self):
        self.apk = utils.deserialize(self.db.load('apk'), self.abs.group)
        self.ask = utils.deserialize(self.db.load('ask'), self.abs.group)

    def get_apk(self):
        return self.db.load('apk')

    def get_public_params(self):
        return self.db.load('publicParams')
        
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
