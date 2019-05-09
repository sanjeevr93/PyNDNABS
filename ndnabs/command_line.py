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

class CommandLine():

    def __init__(self):
        parser = argparse.ArgumentParser(description = 'NDN-ABS managment tool')
        parser.add_argument('-p', '--path', default=os.path.expanduser('~/.ndn/ndnabs.db'),
                            help='''Set path for security database (default: ~/.ndn/ndnabs.db)''')

        sub = parser.add_subparsers(title='command', help=''''NDN-ABS commands''')

        cmd_setup = sub.add_parser('setup', help='''Setup NDN-ABS attribute authority''')
        cmd_setup.add_argument('-f', '--force', action='store_true', default=False, help='''Setup a new authority even if there was one setup before''')
        cmd_setup.add_argument('name', help='''NDN-ABS authority name''')
        cmd_setup.set_defaults(command=self.setup)

        cmd_getPubParams = sub.add_parser('get-pub-params', help='''Get NDN-ABS public parameters (NDN data packet)''')
        cmd_getPubParams.set_defaults(command=self.getPubParams)

        cmd_genSecret = sub.add_parser('gen-secret', help='''Generate secret key for the attribute set (new or extend the set)''')
        cmd_genSecret.add_argument('-s', '--secret', help='''Existing secret key (if attribute set needs to be extended)''')
        cmd_genSecret.add_argument('attribute', help='''Attribute(s) to be included in the set''', nargs='+')
        cmd_genSecret.set_defaults(command=self.genSecret)

        cmd_installPubParams = sub.add_parser('install-pub-params', help='''Install NDN-ABS public parameters''')
        cmd_installPubParams.set_defaults(command=self.installPubParams)

        cmd_installSecret = sub.add_parser('install-secret', help='''Install (replace) the secret key''')
        cmd_installSecret.set_defaults(command=self.installSecret)

        cmd_installSecret = sub.add_parser('export-secret', help='''Export the secret key''')
        cmd_installSecret.add_argument('-v', '--verbose', action='store_true', default=False, help='''Show extended attribute information''')
        cmd_installSecret.set_defaults(command=self.exportSecret)

        args = parser.parse_args()
        try:
            command = args.command
        except:
            parser.print_help()
            exit(1)

        self.db = PickleDb(args.path)

        command(args)

    def setup(self, args):
        aa = AttributeAuthority(self.db)
        if not aa.isSetup() or args.force:
            aa.setup(pyndn.Name(args.name))
            print('Setup successfully completed and public parameters loaded into database')
        else:
            if aa.isSetup():
                print('Authority already set up. Use -f flag to setup a new authority')

    def getPubParams(self, args):
        aa = AttributeAuthority(self.db)
        print(str(aa.get_public_params(), "utf-8"))
        # except:
            # print('Unable to retrieve public parameters')

    def genSecret(self, args):
        aa = AttributeAuthority(self.db)
        attrs = []
        for attribute in args.attribute:
            if not re.match(r'^([a-z]|[A-Z]|[0-9])+$',  attribute):
                print("Invalid character in attribute '%s' (only a-z, A-Z, and 0-9 are allowed)")
                return 1
            attrs.append(attribute.encode('utf-8'))

        oldSecret = None
        if args.secret:
            if args.secret != '-':
                with open(args.secret) as f:
                    oldSecret = base64.b64decode(f.read())
            else:
                oldSecret = base64.b64decode(sys.stdin.read())

        out = aa.gen_attr_keys(attrs, oldSecret)
        print(str(base64.b64encode(out), 'utf-8'))

    def installPubParams(self, args):
        pubParams = sys.stdin.buffer.read()

        signer = Signer(self.db)
        signer.install_public_params(pubParams)

        print ("Installed public parameters for authority %s" % signer.get_public_params_info().getName().toUri())

    def installSecret(self, args):
        secret = base64.b64decode(sys.stdin.read())

        signer = Signer(self.db)
        signer.install_secret(secret)
        print ("Installed secret for [%s] attributes" % ', '.join([str(i, 'utf-8') for i in signer.get_attributes()]))

    def exportSecret(self, args):
        signer = Signer(self.db)

        if args.verbose:
            print("Available attributes: %s" % ', '.join([str(i, 'utf-8') for i in signer.get_attributes()]))
        print(str(base64.b64encode(signer.get_secret()), 'utf-8'))

def main():
    CommandLine()

if __name__ == '__main__':
    main()
