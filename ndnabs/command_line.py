# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from . import ABS, AttributeAuthority, Signer, Verifier, PickleDb

import argparse
import os
import sys

 
     
def main():
    parser = argparse.ArgumentParser(description = "The command line tools for the Attribute authority to perform dedicated operations")
    parser.add_argument('command', help='''NDN-ABS command''', 
        choices=['setup', 
                    'get-public-parameters', 
                    'install-public-parameters', 
                    'generate-secret', 
                    'install-secret', 
                    'export-secret'])
    parser.add_argument('-p', '--path', default=os.path.expanduser('~/.ndn'), help='''Set path for security database (default: ~/.ndn)''')
    
    args = parser.parse_args(sys.argv[1:2])

    db = PickleDb(args.path)

    if args.command == 'setup':
        try:
            self.AttributeAuthority.setup(parser.parse_args(sys.argv[2:]))
        except:
            pass

    elif args.command == 'get-public-parameters':
        try:
            self.AttributeAuthority.get_apk
        except:
            pass
    elif args.command == 'install-public-parameters':
        try:
            self.Signer(db, True)
            self.Verifier(db, True)
        except:
            pass
    elif args.command == 'generate-secret':
        try:
            self.AttributeAuthority.gen_attr_keys(parser.parse_args(sys.argv[2:])) # Have to figure a way to pass attr.
        except: 
            if len(parser.parse_args(sys.argv[3:])) > 2:
                raise ValueError("Attribute list must have max 2 attributes")
    elif args.command == 'install-secret':
        try:
            self.Signer.install_secret(db, True)
        except:
            pass
    elif args.command == 'export-secret':
        try:
            self.Signer.get_secret
        except:
            pass

    # if __name__ == "__main__":
    #     main(argparse)
