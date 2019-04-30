# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
from .utils import serialize, deserialize
from .abs import ABS
import json
import random

class Verification(ABS):

    def __init__(self, group):
        self.group = group

    def verifySupport(self, group):
        self.group = group

        f = open("pubparams.txt", 'r')
        encodedpk = f.read()
        pk = deserialize(encodedpk, group)
        f.close()

        signs = open("signature.txt", 'r')
        encodedsign = signs.read()
        sign = deserialize(encodedsign, group)
        signs.close()

        msgs = open("Message.txt", 'r')
        msg = msgs.read()
        msgs.close()

        pol = open("policy.txt", 'r')
        policy = pol.read()
        pol.close()

        super().verify((pk), sign, msg, policy)
            


