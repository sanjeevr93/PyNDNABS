# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from .abs import ABS
from .attribute_authority import AttributeAuthority

from . import Signer, Verifier, PickleDb, serialize, deserialize

import argparse
import os
import sys
import pyndn
import re
import base64
import time


class Benchmark:
    def __init__(self):
        parser = argparse.ArgumentParser(description = 'NDN-ABS benchmarking tool')
        parser.add_argument('-p', '--path', default=os.path.expanduser('~/.ndn/ndnabs.db'),
                            help='''Set path for security database (default: ~/.ndn/ndnabs.db)''')

        sub = parser.add_subparsers(title='command', help='''Command''')

        cmd_setup = sub.add_parser('setup', help='''Setup attribute authority for with specified name''')
        cmd_setup.add_argument('name', help='''Name of the attribute authority''')
        cmd_setup.set_defaults(command=self.setup)

        cmd_sign = sub.add_parser('sign', help='''Create data packet and sign using the specified attributes''')
        cmd_sign.add_argument('name', help='''Name for the data packet''')
        cmd_sign.add_argument('attribute', nargs='+', help='''Attribute(s) to sign the data packet''')
        cmd_sign.set_defaults(command=self.sign)

        cmd_verify = sub.add_parser('verify', help='''Verify data packet''')
        cmd_verify.set_defaults(command=self.verify)

        args = parser.parse_args()
        try:
            command = args.command
        except:
            parser.print_help()
            exit(1)

        self.db = PickleDb(args.path)

        self.retval = command(args)

    def setup(self, args):
        auth = AttributeAuthority(self.db)

        t = time.process_time()
        auth.setup(pyndn.Name(args.name))
        elapsed_time = time.process_time() - t
        print ("Setup time: %f (seconds)" % elapsed_time)

        return 0

    def sign(self, args):
        data = pyndn.Data()
        data.setName(pyndn.Name(args.name))
        data.setContent(sys.stdin.buffer.read())

        producer = Signer(self.db)

        attributes = [i.encode('utf-8') for i in args.attribute]
        p = time.process_time()
        producer.sign(data, attributes)
        p_elapsed_time = time.process_time() - p
        print ("Signing time: %f (seconds)" % p_elapsed_time)
        print (str(base64.b64encode(data.wireEncode().toBytes()), 'utf-8'))
        return 0

    def verify(self, args):
        data = base64.b64decode(sys.stdin.buffer.read())

        consumer = Verifier(self.db)
        c = time.process_time()
        consumer.verify(data)
        c_elapsed_time = time.process_time() - c
        print ("Verification time: %f (seconds)" % c_elapsed_time)
        return 0

def main():
    benchmark = Benchmark()
    exit(benchmark.retval)

if __name__ == '__main__':
    main()