import unittest
import ndnabs
from charm.toolbox.pairinggroup import PairingGroup

class TestSerialize(unittest.TestCase):

    def setUp(self):
        self.group = PairingGroup('MNT159')
        self.abs = ndnabs.ABS(self.group)

        self.attributes = ['TEST1', 'TEST2', 'TEST3']
        self.tpk = self.abs.trusteesetup(self.attributes)
        self.ask, self.apk = self.abs.authoritysetup(self.tpk)

        self.ska = self.abs.generateattributes(self.ask,['TEST1','TEST2'])
        self.testMessage = 'test message'
        self.testPolicy = 'TEST1 AND TEST2'
        self.signature = self.abs.sign((self.tpk, self.apk), self.ska, self.testMessage, self.testPolicy)

        # sanity check
        self.assertTrue(self.abs.verify((self.tpk, self.apk), self.signature, self.testMessage, self.testPolicy))

    def test_serializeDeserialize(self):
        encoded = ndnabs.serialize(self.signature, self.group)
        # result is different every time, so cannot fix value in the test (library hacking needed)

        self.assertTrue(isinstance(encoded, bytes))

        decoded = ndnabs.deserialize(encoded, self.group)
        self.assertEqual(decoded, self.signature)

if __name__ == '__main__':
    unittest.main()
