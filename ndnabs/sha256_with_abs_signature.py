# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */

from pyndn.generic_signature import GenericSignature
from pyndn.signature import Signature
from pyndn.util.change_counter import ChangeCounter
from pyndn.util.blob import Blob
from pyndn.key_locator import KeyLocator
# from pyndn.validity_period import ValidityPeriod
from pyndn.encoding.tlv.tlv_encoder import TlvEncoder
from pyndn.encoding.tlv.tlv_decoder import TlvDecoder
from pyndn.encoding.tlv_0_2_wire_format import Tlv0_2WireFormat
from pyndn.encoding.tlv.tlv import Tlv

Tlv.SignatureType_Sha256WithAbsSignature = 42
# TlvSha256WithAbsSignature = 42

class Sha256WithAbsSignature(GenericSignature):

    def __init__(self, value = None):
        if value == None:
            self._keyLocator = ChangeCounter(KeyLocator())
            # self._validityPeriod = ChangeCounter(ValidityPeriod())
            self._signature = Blob()
        elif isinstance(value, Sha256WithAbsSignature):
            # Copy its values.
            self._keyLocator = ChangeCounter(KeyLocator(value.getKeyLocator()))
            # self._validityPeriod = ChangeCounter(ValidityPeriod(value.getValidityPeriod()))
            self._signature = value._signature
        elif isinstance(value, GenericSignature):
            self.wireDecode(value.getSignatureInfoEncoding().toBuffer())
            self._signature = value.getSignature()
        else:
            raise RuntimeError(
              "Unrecognized type for Sha256WithAbsSignature constructor: " +
              str(type(value)))

        self._changeCount = 0

    def clone(self):
        """
        Create a new Sha256WithAbsSignature which is a copy of this object.

        :return: A new object which is a copy of this object.
        :rtype: Sha256WithAbsSignature
        """
        return Sha256WithAbsSignature(self)

    def getKeyLocator(self):
        """
        Get the key locator.

        :return: The key locator.
        :rtype: KeyLocator
        """
        return self._keyLocator.get()

    # def getValidityPeriod(self):
    #     """
    #     Get the validity period.

    #     :return: The validity period.
    #     :rtype: ValidityPeriod
    #     """
    #     return self._validityPeriod.get()

    def getSignature(self):
        """
        Get the data packet's signature bytes.

        :return: The signature bytes as a Blob, which maybe isNull().
        :rtype: Blob
        """
        return self._signature

    def setKeyLocator(self, keyLocator):
        """
        Set the key locator to a copy of the given keyLocator.

        :param KeyLocator keyLocator: The KeyLocator to copy.
        """
        self._keyLocator.set(KeyLocator(keyLocator))
        self._changeCount += 1

    # def setValidityPeriod(self, validityPeriod):
    #     """
    #     Set the validity period to a copy of the given ValidityPeriod.

    #     :param ValidityPeriod validityPeriod: The ValidityPeriod which is copied.
    #     """
    #     self._validityPeriod.set(ValidityPeriod(validityPeriod))
    #     self._changeCount += 1

    def setSignature(self, signature):
        """
        Set the signature bytes to the given value.

        :param signature: The array with the signature bytes. If signature is
          not a Blob, then create a new Blob to copy the bytes (otherwise
          take another pointer to the same Blob).
        :type signature: A Blob or an array type with int elements
        """
        self._signature = (signature if isinstance(signature, Blob)
                           else Blob(signature))
        self._changeCount += 1

    def clear(self):
        self._keyLocator.get().clear()
        self._signature = Blob()
        self._changeCount += 1

    def getChangeCount(self):
        """
        Get the change count, which is incremented each time this object
        (or a child object) is changed.

        :return: The change count.
        :rtype: int
        """
        # Make sure each of the checkChanged is called.
        changed = self._keyLocator.checkChanged()
        # changed = self._validityPeriod.checkChanged() or changed
        if changed:
            # A child object has changed, so update the change count.
            self._changeCount += 1

        return self._changeCount

    def wireEncode(self):
        encoder = TlvEncoder(500)
        saveLength = len(encoder)
        
        # if self.getValidityPeriod().hasPeriod():
        #     Tlv0_2WireFormat._encodeValidityPeriod(self.getValidityPeriod(), encoder)
        Tlv0_2WireFormat._encodeKeyLocator(Tlv.KeyLocator, self.getKeyLocator(), encoder)
        encoder.writeNonNegativeIntegerTlv(Tlv.SignatureType, Tlv.SignatureType_Sha256WithAbsSignature)
        encoder.writeTypeAndLength(Tlv.SignatureInfo, len(encoder) - saveLength)

        self.setSignatureInfoEncoding(Blob(encoder.getOutput(), False), Tlv.SignatureType_Sha256WithAbsSignature)

    def wireDecode(self, wire):
        decoder = TlvDecoder(wire)

        beginOffset = decoder.getOffset()
        endOffset = decoder.readNestedTlvsStart(Tlv.SignatureInfo)

        signatureType = decoder.readNonNegativeIntegerTlv(Tlv.SignatureType)
        if signatureType != Tlv.SignatureType_Sha256WithAbsSignature:
            raise RuntimeError("Invalid SignatureType code: expected %d, got %d" % (Tlv.SignatureType_Sha256WithAbsSignature, signatureType))

        keyLocator = KeyLocator()
        Tlv0_2WireFormat._decodeKeyLocator(Tlv.KeyLocator, keyLocator, decoder, True)

        self._keyLocator = ChangeCounter(keyLocator)

        # if decoder.peekType(Tlv.ValidityPeriod_ValidityPeriod, endOffset):
        #     Tlv0_2WireFormat._decodeValidityPeriod(
        #         signatureInfo.getValidityPeriod(), decoder)

        decoder.finishNestedTlvs(endOffset)

    # Create managed properties for read/write properties of the class for more pythonic syntax.
    keyLocator = property(getKeyLocator, setKeyLocator)
    signature = property(getSignature, setSignature)
