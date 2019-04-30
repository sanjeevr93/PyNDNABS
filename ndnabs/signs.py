# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import json
import sys
import random
from .abs import ABS
from .utils import deserialize,serialize
from .msp import MSP

class Signs(ABS):

    def __init__(self,group):
        self.group = group
        

    def SignSupport(self, group):
        self.group = group

        pub = open("pubparams.txt", 'r')
        encodedpk = pub.read()
        pk = deserialize(encodedpk, group)
        pub.close()

        ssk = open("ska.txt", 'r')
        encodedska = ssk.read()
        ska = deserialize(encodedska, group)
        ssk.close()

        msgs = open("Message.txt", 'r')
        msg = msgs.read()
        msgs.close()

        pol = open("policy.txt", 'r')
        policy = pol.read()
        pol.close()

        sign = super().sign(pk, ska, msg, policy)

        encsign = serialize(sign, group)

        a = open("signature.txt", 'w')
        a.write(encsign)
        a.close()