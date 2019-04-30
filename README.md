# PyNDNABS
Python Implementation of NDN-ABS

## NDN Packet format extensions

Following are extensions of the [NDN packet format specification](http://named-data.net/doc/NDN-packet-spec/current/signature.html) regarding signature types.

### Signature Type

| Value  | Reference  | Description  |
|--------|------------|--------------|
| 42     | `SignatureSha256WithAbs` | Integrity and provenance protection using Attribute-Based Signature over a SHA-256 digest


### `SignatureSha256WithAbs`

`SignatureSha256WithAbs` defines an Attribute-Based signature signature mechanism that is calculated over the SHA256 hash of the `Name`, `MetaInfo`, `Content`, and `SignatureInfo` TLVs. The signature algorithm is defined in [Maji, Hemanta K., Manoj Prabhakaran, and Mike Rosulek. "Attribute-based signatures." Cryptographers’ track at the RSA conference. Springer, Berlin, Heidelberg, 2011.](https://eprint.iacr.org/2010/595.pdf).

The `TLV-VALUE` of `SignatureType` is 42

`KeyLocator` is required and must follow the format:

    <attribute-authority-prefix>/ABS/42=policy/<attribute-policy>

where

- `<attribute-authority-prefix>` is an arbitrary name prefix of an attribute authority, provided that `<attribute-authority-prefix>/ABS/42=pp/<version>` names a data packet that carries public parameters of the authority.  This data packet can be further signed by ABS or other types of signature and should be considered trusted based on configured trust schema.

- `<attribute-policy>` is defined as

        AttributePolicy = Attribute *ExtraAttribute
        ExtraAttribute = BooleanOperator Attribute

        Attribute = DIGIT / LCASELETTER / UCASELETTER
        DIGIT = %x30-39 ; 0-9
        LCASELETTER = %x61-7a ; 'a'-'z'
        UCASELETTER = %x41-5a ; 'A'-'Z'

        BooleanOperator = "&" / "|"

For example,

        /ndn/edu/fiu/ABS/42=policy/student&2019

Represents an ABS policy under `/ndn/edu/fiu` authority (i.e., there is `/ndn/edu/fiu/ABS/42=pp/<version>` data packet carrying public parameters of the attribute authority), signing using two attributes combined with "AND" boolean operator: "student" and "2019".

Note attributes are case sensitive: "student" and "Student" refer to different attributes.
