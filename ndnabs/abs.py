# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This implementation is largely based on https://github.com/TBD/TBD

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import json
import random

class ABS:
    '''
    2B done
    '''
    def __init__(self,group):
        self.group = group

    def generateattributes(self, ask, attriblist):
        '''
        returns signing key SKa
        '''
        ska = {}

        Kbase = self.group.random(G1) #"random generator" within G
        ska['Kbase'] = Kbase

        ska['K0'] = Kbase ** (1/ask['a0'])

        for i in attriblist:
            number = ask['atr'][i]
            ska['K{}'.format(number)] = Kbase ** (1 / (ask['a'] + number * ask['b']))

        return ska

    def sign(self, pk, ska, message, policy): #pk = (tpk,apk)
        '''
        return signature
        '''
        tpk,apk = pk
        lambd = {}
        
        M = [[1, 1], [0, -1]]
        with open("selectattr.txt", 'r') as filehandle:  
            u = filehandle.readlines()

        mu = self.group.hash(message+policy)

        r = []
        for i in range(len(M)+1):
            r.append(self.group.random(ZR))

        lambd['Y'] = ska['Kbase'] ** r[0]
        lambd['W'] = ska['K0'] ** r[0]

        for i in range(1,len(M)+1):
            end = 0
            multi = ((apk['C'] * (tpk['g'] ** mu)) ** r[i])
            try: #this fills in for the v vector
                end = multi * (ska['K{}'.format(tpk['atr'][u[i-1]])] ** r[0])
            except KeyError:
                end = multi
            lambd['S{}'.format(i)] = end

        for j in range(1,len(M[0])+1):
            end = 0
            for i in range(1,len(M)+1):
                base = apk['A{}'.format(j)] * (apk['B{}'.format(j)] ** tpk['atr'][u[i-1]])
                exp = M[i-1][j-1] * r[i]
                end = end * (base ** exp)
            lambd['P{}'.format(j)] = end

        return lambd

    def verify(self, pk, sign, message, policy):
        '''
        return bool
        '''

        M = [[1, 1], [0, -1]]
        with open("selectattr.txt", 'r') as filehandle:  
            u = filehandle.readlines()

        mu = self.group.hash(message+policy)

        if sign['Y']==0 or pair(sign['Y'],pk['h0']) != pair(sign['W'],pk['A0']):
            return False
        else:
            sentence = True
            for j in range(1,len(M[0])+1):
                multi = 0
                for i in range(1,len(M)+1):
                    a = sign['S{}'.format(i)]
                    b = (pk['A{}'.format(j)] * (pk['B{}'.format(j)] ** pk['atr'][u[i-1]])) ** M[i-1][j-1]
                    multi = multi * pair(a,b)
                try:
                    after = pair(pk['C'] * pk['g'] ** mu, sign['P{}'.format(j)])
                    pre = pair(sign['Y'], pk['h{}'.format(j)])
                    if j == 1:
                        if multi != (pre * after):#after:
                            sentence = False
                    else:
                        if multi != (after):
                            sentence = False
                except Exception as err:
                    print(err)
            return sentence
    
    def getMSP(self,matrix,attributes):

        '''
        returns the MSP that fits given policy

        target vector (1,0,....,0)

        Current implementation has a policy with 2 attr seperated by AND
        Thus, we hard-code the MSP in here
        '''
        u = {}
        u = attributes
        return matrix,u

    

    '''

    def trusteesetup(self, attributes):

        Run by signature trustees
        returns the trustee public key

        Notice: Certain variables have been removed completely.
        G and H are handled by G1 and G2 type generators respectively,
        and the hash function is a generic one for the curve and can
        be derived from the group attribute.

        Attributes have to be appended to the end for global-ness

        tpk = {}
        tmax = 2 * len(attributes)

        tpk['g'] = self.group.random(G1)
        for i in range(tmax+1): #provide the rest of the generators
            tpk['h{}'.format(i)] = self.group.random(G2)

        attriblist = {}
        counter = 2
        for i in attributes:
            attriblist[i] = counter
            counter += 1

        tpk['atr'] = attriblist

        return tpk

    def authoritysetup(self, tpk):

        Run by attribute-giving authority, takes tpk as parametre
        returns attribute master key and public key

        ask = {}
        apk = {}
        tmax = 2 * len(tpk['atr'])

        group = self.group
        a0,a,b = group.random(ZR), group.random(ZR), group.random(ZR)
        ask['a0'] = a0
        ask['a'] = a
        ask['b'] = b
        ask['atr'] = tpk['atr'] #this is for ease of usage

        apk['A0'] = tpk['h0'] ** a0
        for i in range(1,tmax+1): #rest of the whateverifys
            apk['A{}'.format(i)] = tpk['h{}'.format(i)] ** a

        for i in range(1,tmax+1):
            apk['B{}'.format(i)] = tpk['h{}'.format(i)] ** b

        apk['C'] = tpk['g'] ** group.random(ZR) #C = g^c at the end

        return ask,apk
    '''