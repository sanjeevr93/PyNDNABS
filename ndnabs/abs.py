# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import json
import random

from . import g_ndnAbsPairingGroup

class AttributeKeyNotAvailable(Exception):
    pass

class ABS:
    '''
    2B done
    '''
    def __init__(self):
        self.group = g_ndnAbsPairingGroup

    def authSetup(self):
        '''
        Run by Attribute Issuing Authority
        
        Store the Public Key (Apk) and Secret key (Ask) into disk

        We define a single authority who defines the public parameters 
        that will be used in the system.
        '''
        apk = {}
        ask = {}
        tmax = 4

        apk['g'] = self.group.random(G1)
        for i in range(tmax + 1): #provide the rest of the generators
            apk['h{}'.format(i)] = self.group.random(G2)

        a0,a,b = self.group.random(ZR), self.group.random(ZR), self.group.random(ZR)
        ask['a0'] = a0
        ask['a'] = a
        ask['b'] = b

        apk['A0'] = apk['h0'] ** a0
        for i in range(1, tmax + 1): #rest of the whateverifys
            apk['A{}'.format(i)] = apk['h{}'.format(i)] ** a

        for i in range(1,tmax+1):
            apk['B{}'.format(i)] = apk['h{}'.format(i)] ** b

        apk['C'] = apk['g'] ** self.group.random(ZR) #C = g^c at the end

        return apk, ask
        
    def generateattributes(self, ask, attributes, Kbase = None):
        '''
        returns signing key SKa
        '''
        ska = {}

        if not Kbase:
            Kbase = self.group.random(G1) # "random generator" within G

        ska['Kbase'] = Kbase
        ska['K0'] = Kbase ** (1 / ask['a0'])

        for i in attributes:
            u = self.group.hash(i)
            ska['K{}'.format(u)] = Kbase ** (1 / (ask['a'] + u * ask['b']))

        return ska

    def getCheatyMsp(self, message, attributes):
        if len(attributes) != 2:
            raise RuntimeError("Must supply exactly two attributes for ABS sign/verify")

        M = [[1, 1], [0, -1]]
        u = [self.group.hash(i) for i in attributes]
        mu = self.group.hash(message + b' AND '.join(attributes))
        return M, u, mu

    def sign(self, pk, ska, message, attributes):
        '''
        return signature
        '''
        lambd = {}

        M, u, mu = self.getCheatyMsp(message, attributes)

        # Under current assumption (2 attributes combined with 'AND'), all 'ska' must include keys for all requested attributes
        for i in range(len(attributes)):
            if 'K{}'.format(u[i]) not in ska.keys():
                raise AttributeKeyNotAvailable(attributes[i]) 

        r = []
        for i in range(len(M) + 1):
            r.append(self.group.random(ZR))

        lambd['Y'] = ska['Kbase'] ** r[0]
        lambd['W'] = ska['K0'] ** r[0]

        for i in range(1, len(M) + 1):
            end = 0
            multi = ((pk['C'] * (pk['g'] ** mu)) ** r[i])
            try: #this fills in for the v vector
                end = multi * (ska['K{}'.format(u[i-1])] ** r[0])
            except KeyError:
                end = multi
            lambd['S{}'.format(i)] = end

        for j in range(1,len(M[0])+1):
            end = 0
            for i in range(1,len(M)+1):
                base = pk['A{}'.format(j)] * (pk['B{}'.format(j)] ** u[i-1])
                exp = M[i-1][j-1] * r[i]
                end = end * (base ** exp)
            lambd['P{}'.format(j)] = end

        return lambd

    def verify(self, pk, sign, message, attributes):
        '''
        return bool
        '''

        M, u, mu = self.getCheatyMsp(message, attributes)

        if sign['Y']==0 or pair(sign['Y'], pk['h0']) != pair(sign['W'], pk['A0']):
            return False
        else:
            sentence = True
            for j in range(1,len(M[0])+1):
                multi = 0
                for i in range(1,len(M)+1):
                    a = sign['S{}'.format(i)]
                    b = (pk['A{}'.format(j)] * (pk['B{}'.format(j)] ** u[i-1])) ** M[i-1][j-1]
                    multi = multi * pair(a,b)

                
                after = pair(pk['C'] * pk['g'] ** mu, sign['P{}'.format(j)])
                pre = pair(sign['Y'], pk['h{}'.format(j)])
                if j == 1:
                    if multi != (pre * after):#after:
                        sentence = False
                else:
                    if multi != (after):
                        sentence = False
            return sentence
