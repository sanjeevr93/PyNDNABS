# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

from . import ABS, AttributeAuthority, Signer, Verifier, PickleDb
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
        parser.add_argument("command", help='''NDN-ABS command''', choices=["path", "setup", "getPubParams", "installPubParams", "genSecret", 
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
            print('Success')
            print(args.Setup)
            self.aa = AttributeAuthority(DB)
            print(DB)
            self.aa.setup(pyndn.Name(args.Setup))
            print('Success')
        except:
            pass

    def getPubParams(self): 
        parser = argparse.ArgumentParser(description = "Retrieve Public Parameters from repo")
        parser.add_argument('-g', '--GetPub', action='store')
        try:
            self.aa = AttributeAuthority(DB)
            print(DB)
            self.aa.get_public_params()
        except:
            raise AssertionError


    def installPubParams(self):
        parser = argparse.ArgumentParser(description = "Install the Public Parameters retrieved from repo")
        parser.add_argument('-i', '--InstallPub', action='store')
        try:
            self.aa = AttributeAuthority(DB)
            self.signer = Signer(DB)
            self.signer.install_public_params(self.aa.get_public_params())
            print('Success')

            # self.verifier = Verifier(DB)
            # self.verifier.install_public_params(self.aa.get_public_params())
        except:
            pass


    def genSecret(self):
        parser = argparse.ArgumentParser(description = "Generate Secret Signing key")
        parser.add_argument('-gs', '--GenSec', nargs=2, action='store')
        args = parser.parse_args(sys.argv[2:])
        try:
            self.aa = AttributeAuthority(DB)
            abc = self.aa.gen_attr_keys(args.GenSec) # Not sure if this passes a list of attributes or not
            print(abc)
        except: 
            if len(args.GenSec) > 2:
                raise ValueError("Attribute list must have max 2 attributes")

    
    def installSecret(self):
        parser = argparse.ArgumentParser(description = "Install the Secret Signing key")
        parser.add_argument('-is', '--InstallSec', action='store')
        try:
            self.signer = Signer(DB)
            self.signer.install_secret(Commandline.genSecret.abc)
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
