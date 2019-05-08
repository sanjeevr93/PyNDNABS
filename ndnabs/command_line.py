# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from . import ABS, AttributeAuthority, Signer, Verifier, PickleDb, serialize, deserialize
from . import db

import argparse
import os
import sys
import pyndn
import tempfile
    
class Commandline():

    def __init__(self):
        self.DB = db

        parser = argparse.ArgumentParser(description = "The command line tools for the Attribute authority to perform dedicated operations")
        parser.add_argument("command", help='''NDN-ABS command''', choices=["setup", "getPubParams", "installPubParams", "genSecret", 
                                "installSecret"])
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            exit(1)
        getattr(self, args.command)()

    # def path(self):
    #     parser = argparse.ArgumentParser(description = "DB path")
    #     parser.add_argument('-p', '--Path', default=os.path.expanduser(os.path.abspath('~/.ndn')), help='''Set path for security database (default: ~/.ndn)''', action='store')
    #     args = parser.parse_args(sys.argv[2:])
    #     db = PickleDb(args.Path)
    #     self.aa = AttributeAuthority(db)
    #     print(db)

    def setup(self):
        parser = argparse.ArgumentParser(description = "Attribute authority setup")
        parser.add_argument('-s', '--Setup', action='store')
        args = parser.parse_args(sys.argv[2:])
        try:
            self.aa = AttributeAuthority(self.DB)
            self.aa.setup(pyndn.Name(args.Setup))
            print('Setup Successfully completed and public parameters loaded into database')
        except:
            print('Missing a valid Attr. authority name or setup failed')

    def getPubParams(self): 
        parser = argparse.ArgumentParser(description = "Retrieve Public Parameters from repo")
        parser.add_argument('-g', '--GetPub', action='store')
        try:
            self.aa = AttributeAuthority(self.DB)
            params =  deserialize(self.aa.get_public_params(), self.aa.group)
            print(params)
        except:
            print('Unable to retrieve public parameters')

    def installPubParams(self):
        parser = argparse.ArgumentParser(description = "Install the Public Parameters retrieved from repo")
        parser.add_argument('-i', '--InstallPub', action='store')
        try:
            self.aa = AttributeAuthority(self.DB)
            self.signer = Signer(DB)
            self.signer.install_public_params(self.aa.get_public_params())
            print('Public parameters successfully installed by Signer')

            self.verifier = Verifier(DB)
            self.verifier.install_public_params(self.aa.get_public_params())
            print('Public parameters successfully installed by Verifier')
        except:
            pass


    def genSecret(self):
        parser = argparse.ArgumentParser(description = "Generate Secret Signing key")
        parser.add_argument('-gs', '--GenSec', nargs=2, action='store')
        args = parser.parse_args(sys.argv[2:])
        try:
            self.aa = AttributeAuthority(self.DB)
            self.aa.gen_attr_keys(args.GenSec) # Not sure if this passes a list of attributes or not
            print('Secret signing key generated successfully')
        except: 
            if len(args.GenSec) > 2:
                raise ValueError("Attribute list must have max 2 attributes")

    
    def installSecret(self):
        parser = argparse.ArgumentParser(description = "Install the Secret Signing key")
        parser.add_argument('-is', '--InstallSec', action='store')
        try:
            self.signer = Signer(DB)
            self.signer.install_secret(Commandline.genSecret)
            if Commandline.genSecret.abc:
                print('Success')
            else:
                self.assertRaises(ndnabs.AttributeKeyNotAvailable)
        except:
            pass


    # def exportSecret(self):
    #     parser = argparse.ArgumentParser(description = "Install the Secret Signing key")
    #     parser.add_argument('-is', '--InstallSec', action='store_true')
    #     try:
    #         self.signer = Signer(Commandline.path.db)
    #         tmp = self.Signer.get_secret()
    #         if tmp:
    #             print('Success')
    #         else:
    #             raise ValueError
    #     except:
    #         pass


if __name__ == '__main__':
    Commandline()
