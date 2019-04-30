# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import random

class MSP: 
    
    def getMSP(self,policy,attributes):

        '''
        returns the MSP that fits given policy

        utilizes the charm-crypto "policy -> binary tree" structure which has to be
        gone through only once

        target vector (1,0,....,0)
        '''
        u = {}
        counter = 0
        for i in attributes:
            u[counter] = i
            u[i] = counter
            counter += 1
        '''
        Current implementation has a policy with 2 attr seperated by AND
        Thus, we hard-code the MSP in here
        '''
        matrix = [[1, 1], [0, -1]]

        print(matrix)
        return matrix,u

    
        '''
        Code block to be appended in case we want to use a more dynamic approach
        
        parser = PolicyParser()
        tree = parser.parse(policy)

        matrix = [] #create matrix as a dummy first (easy indexing)
        for i in range(len(attributes)):
            matrix.append([])

        counter = [1]
        def recursivefill(node,vector): #create MSP compatible rows
            if node.getNodeType() == OpType.ATTR:
                text = node.getAttribute()
                temp = list(vector)
                matrix[u[text]] = temp
            elif node.getNodeType() == OpType.OR:
                recursivefill(node.getLeft(),vector)
                recursivefill(node.getRight(),vector)
            else: #AND here, right?
                temp = list(vector)
                while(len(temp)<counter[0]):
                    temp.append(0)
                emptemp = []
                while(len(emptemp)<counter[0]):
                    emptemp.append(0)
                temp.append(1)
                emptemp.append(-1)
                counter[0] += 1
                recursivefill(node.getLeft(),temp)
                recursivefill(node.getRight(),emptemp)
        recursivefill(tree,[1])
        '''