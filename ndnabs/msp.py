# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
from .abs import ABS
import random


class MSP(ABS): 
    
    def MSPSupport(self):

        '''
        returns the MSP that fits given policy

        utilizes the charm-crypto "policy -> binary tree" structure which has to be
        gone through only once

        target vector (1,0,....,0)
        '''
        
        with open("selectattr.txt", 'r') as filehandle:  
            u = filehandle.readlines()
        
        '''
        Current implementation has a policy with 2 attr seperated by AND
        Thus, we hard-code the MSP in here
        '''
        matrix = [[1, 1], [0, -1]]

        super().getMSP(matrix,u)


