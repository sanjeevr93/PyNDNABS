# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import json
import random
from .abs import ABS
from .utils import deserialize, serialize

class AttrGen(ABS):

    def __init__(self,group):
        self.group = group
        self.abs = ABS(self.group)


    def generateattr(self, group):
        self.group = group
        '''
        returns signing key SKa
        '''
        with open("selectattr.txt", 'r') as filehandle:  
            attr = filehandle.readlines()

        with open("secretkeys.txt", 'r') as filehands:
            encask = filehands.read()

        ask = deserialize(encask, group)

        ska = {}
        ska = super().generateattributes(ask,attr)
    
        encodedska = serialize(ska, self.group)

        f = open("ska.txt", 'w')
        f.write(encodedska)
        f.close()
