#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 11:41:31 2020

@author: CHEKINI Hakima && BEN SAADA Maryem
"""

from OpenSSL import SSL
from cryptography.fernet import Fernet

import os
#  print SSL Certificate Paths.
#print (SSL._CERTIFICATE_PATH_LOCATIONS)

#OpenSSL.crypto.PKey().generate_key(TYPE_RSA, 1024)
from OpenSSL import crypto

key = crypto.PKey()
crypto.PKey.generate_key(key, crypto.TYPE_RSA, 1024)

print(str(key))


pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
print(len(pubKeyString))
pubKeyFile=open("clePub.pub.pem", "w")
pubKeyFile.write(pubKeyString)
pubKeyFile.close()

privateKeyString = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
print(len(privateKeyString))
privateKeyFile=open("clePrv.pem", "w")
privateKeyFile.write(privateKeyString)
privateKeyFile.close()

#fernet=Fernet(privateKeyString)
#encrypted= fernet.encrypt("hello this is a test msg")
#print encrypted


