import unittest
import ndnabs

class TestSerialize(unittest.TestCase):

    def setUp(self):
        self.abs = ndnabs.ABS()

        self.attributes = ['TEST1', 'TEST2', 'TEST3']
        self.apk, self.ask = self.abs.authSetup()

        self.ska = self.abs.generateattributes(self.ask, ['TEST1','TEST2'])
        self.testMessage = b'test message'
        self.testAttributes = ['TEST1', 'TEST2']
        self.signature = self.abs.sign(self.apk, self.ska, self.testMessage, self.testAttributes)

        # sanity check
        self.assertTrue(self.abs.verify(self.apk, self.signature, self.testMessage, self.testAttributes))

    def test_serializeDeserialize(self):
        encoded = ndnabs.serialize(self.signature, self.abs.group)
        # result is different every time, so cannot fix value in the test (library hacking needed)

        self.assertTrue(isinstance(encoded, bytes))

        decoded = ndnabs.deserialize(encoded, self.abs.group)
        self.assertEqual(decoded, self.signature)

if __name__ == '__main__':
    unittest.main()
