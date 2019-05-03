import unittest
import ndnabs

import sys
import os
import tempfile
import shutil

class TestSigner(unittest.TestCase):

    testMessage = b'Hello, world!'
    
    def setUp(self):
        db = ndnabs.PickleDb('%s/test_authority.db' % os.path.dirname(os.path.realpath(__file__)))
        self.aa = ndnabs.AttributeAuthority(db)

        fd, self.tmpDbPath = tempfile.mkstemp()
        os.close(fd)
        shutil.copy('%s/test_signer.db' % os.path.dirname(os.path.realpath(__file__)), self.tmpDbPath)
        print (self.tmpDbPath)
        
        db = ndnabs.PickleDb(self.tmpDbPath)
        self.signer = ndnabs.Signer(db)

    def tearDown(self):
        os.remove(self.tmpDbPath)
        
    def test_sign(self):
        signature = self.signer._sign(self.testMessage, [b'Monday', b'Tuesday'])

        with self.assertRaises(ndnabs.AttributeKeyNotAvailable):
            self.signer._sign(self.testMessage, [b'MONDAY', b'Tuesday'])

        oldSecret = self.signer.get_secret()
        newSecret = self.aa.gen_attr_keys([b'MONDAY'], oldSecret)

        self.signer.install_secret(newSecret)
        self.signer._sign(self.testMessage, [b'MONDAY', b'Tuesday'])

if __name__ == '__main__':
    unittest.main()
