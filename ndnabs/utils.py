# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

import base64
import pickle
from charm.core.engine.util import serializeObject, deserializeObject

def reDecodeBase64Dict(Object):
    '''base64 decode (not quite sure why the library automatically base64'ing)'''
    out = {}
    for i in Object.keys():
        if i == 'attributes':
            out[i] = Object[i]
        else:
            x = Object[i].split(b':')
            out[i]=[x[0], base64.b64decode(x[1])]
    return out

def reEncodeBase64Dict(Object):
    '''base64 encode (not quite sure why the library automatically expects base64'ing)'''
    out = {}
    for i in Object.keys():
        if i == 'attributes':
            out[i] = Object[i]
        else:
            out[i]=b'%s:%s' % (Object[i][0], base64.b64encode(Object[i][1]))
    return out

def serialize(Object, group):
    serializedDictWithBase64 = serializeObject(Object, group)
    serializedDict = reDecodeBase64Dict(serializedDictWithBase64)
    return pickle.dumps(serializedDict)

def deserialize(bytes, group):
    serializedDict = pickle.loads(bytes)
    serializedDictWithBase64 = reEncodeBase64Dict(serializedDict)
    return deserializeObject(serializedDictWithBase64, group)
