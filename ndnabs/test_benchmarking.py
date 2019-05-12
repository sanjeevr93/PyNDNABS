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
import csv


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
        csvData = []
        name = args.name
        for i in range(100):
            name = name + '%s' % i
            t = time.process_time()
            auth.setup(pyndn.Name(name))
            csvData.append(str(time.process_time() - t))
        with open('setup.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows([csvData])
        return 0

    def sign(self, args):
        data = pyndn.Data()
        data.setName(pyndn.Name(args.name))
        data.setContent(sys.stdin.buffer.read())
        
        attributes = [args.attribute]
        producer = Signer(self.db)

        csvData = []

        for i in range(100):
            attributes.append('%s' % i)
            attr = [i.encode('utf-8') for i in attributes]
            p = time.process_time()
            producer.sign(data, attr)
            csvData.append(str(time.process_time() - p)) 
        with open('signingtime.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows([csvData])
        return 0

    def verify(self, args):
        data = base64.b64decode(sys.stdin.buffer.read())

        csvData = []

        for i in range(100):
            consumer = Verifier(self.db)
            c = time.process_time()
            consumer.verify(data)
            csvData.append(str(time.process_time() - c))
        with open('verifytime.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows([csvData])
        return 0

def main():
    benchmark = Benchmark()
    exit(benchmark.retval)

if __name__ == '__main__':
    main()