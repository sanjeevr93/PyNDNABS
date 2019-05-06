# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from . import ABS, AttributeAuthority, Signer, Verifier, PickleDb

import argparse
import os
import sys
    
def main():
    parser = argparse.ArgumentParser(description = "The command line tools for the Attribute authority to perform dedicated operations")
    parser.add_argument('-p', '--path', default=os.path.expanduser(os.path.abspath('~/.ndn')), help='''Set path for security database (default: ~/.ndn)''')
    # parser.add_argument("-c", '--command', help='''NDN-ABS command''', 
    #     choices=["setup", 
    #                 "get-public-parameters", 
    #                 "install-public-parameters", 
    #                 "generate-secret", 
    #                 "install-secret", 
    #                 "export-secret"], nargs='*')
    parser.add_argument("-s", '--setup', help='''Authority Setup''', nargs=1)
    parser.add_argument("-g", '--getPubParams', help='''Get Public Parameters''', nargs='?')
    parser.add_argument("-i", '--installPubParams', help='''Install Public Parameters''', nargs='?' )
    parser.add_argument("-gs", '--genSecret', help='''Generate Secret''', nargs='+')
    parser.add_argument("-is", '--installSecret', help='''Install Secret''', nargs='?')
    parser.add_argument("-es", '--exportSecret', help='''Export Secret''', nargs='?')

    args = parser.parse_args()

    db = PickleDb(args.path)
    # print(db)
    # print(args.path)

    if args.setup:
        try:
            # print("Setup successful")
            # print(args.setup)
            self.AttributeAuthority.setup(args.setup)
        except:
            pass

    elif args.getPubParams:
        try:
            # print("Entered GetPubParams")
            # print(args.getPubParams)
            # print(args.path)
            aa = AttributeAuthority.get_apk
            # print(aa)
        except:
            raise AssertionError

    elif args.installPubParams:
        try:
            self.Signer._install_pk
            self.Verifier.install_public_parameters
        except:
            raise ValueError

    elif args.genSecret:
        try:
            # print(parser.parse_args(sys.argv[2:]))
            self.AttributeAuthority.gen_attr_keys(parser.parse_args(sys.argv[2:])) # Not sure if this passes a list of attributes or not
        except: 
            if len(parser.parse_args(sys.argv[3:])) > 2:
                raise ValueError("Attribute list must have max 2 attributes")
    
    elif args.installSecret:
        try:
            self.Signer.install_secret(db, True)
        except:
            pass

    elif args.exportSecret:
        try:
            self.Signer.get_secret
        except:
            pass

if __name__ == "__main__":
    main()
