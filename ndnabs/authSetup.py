# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
from charm.core.engine.util import serializeObject, deserializeObject
import json
import random
from .utils import serialize

class AuthSetup:

    def __init__(self,group):
        self.group = group

    def authSetup(self,group):
        '''
        Run by Attribute Issuing Authority
        
        Store the Public Key (Apk) and Secret key (Ask) into disk

        We define a single authority who defines the public parameters 
        that will be used in the system.
        '''
        apk = {}
        ask = {}
        tmax = 10

        apk['g'] = self.group.random(G1)
        for i in range(tmax+1): #provide the rest of the generators
            apk['h{}'.format(i)] = self.group.random(G2)

        a0,a,b = self.group.random(ZR), self.group.random(ZR), self.group.random(ZR)
        ask['a0'] = a0
        ask['a'] = a
        ask['b'] = b
        #ask['atr'] = tpk['atr'] #this is for ease of usage

        apk['A0'] = apk['h0'] ** a0
        for i in range(1,tmax+1): #rest of the whateverifys
            apk['A{}'.format(i)] = apk['h{}'.format(i)] ** a

        for i in range(1,tmax+1):
            apk['B{}'.format(i)] = apk['h{}'.format(i)] ** b

        apk['C'] = apk['g'] ** self.group.random(ZR) #C = g^c at the end

        # Have to serialize the content and store in disk

        encodedapk = serialize(apk, group)
        print(encodedapk)
        encodedask = serialize(ask, group)
        print(encodedask)

        f = open("pubparams.txt", 'w')
        f.write(encodedapk)
        f.close()

        secr = open("secretkeys.txt", 'w')
        secr.write(encodedask)
        secr.close()

        return encodedapk, encodedask
