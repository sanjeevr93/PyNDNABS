import unittest
import ndnabs

import sys
import os
import tempfile
import shutil

class TestVerifier(unittest.TestCase):

    testMessage = b'Hello, world!'
    
    def setUp(self):
        db = ndnabs.PickleDb('%s/test_authority.db' % os.path.dirname(os.path.realpath(__file__)))
        self.aa = ndnabs.AttributeAuthority(db)

        db = ndnabs.PickleDb('%s/test_signer.db' % os.path.dirname(os.path.realpath(__file__)))
        self.signer = ndnabs.Signer(db)

        fd, self.tmpDbPath = tempfile.mkstemp()
        os.close(fd)
        shutil.copy('%s/test_verifier.db' % os.path.dirname(os.path.realpath(__file__)), self.tmpDbPath)
        print (self.tmpDbPath)
        
        db = ndnabs.PickleDb(self.tmpDbPath)
        self.verifier = ndnabs.Verifier(db)

    def tearDown(self):
        os.remove(self.tmpDbPath)
        
    def test_verify(self):
        signature = self.signer._sign(self.testMessage, [b'Monday', b'Tuesday'])

        self.assertTrue(self.verifier.verify(signature, self.testMessage, [b'Monday', b'Tuesday']))
        self.assertFalse(self.verifier.verify(signature, b'not a message', [b'Monday', b'Tuesday']))
        self.assertFalse(self.verifier.verify(signature, self.testMessage, [b'Monday', b'Wednesday']))

if __name__ == '__main__':
    unittest.main()
