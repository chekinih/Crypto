#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:48:46 2020

@author: 11607156
"""

#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

import os
import io

def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1234               # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
msg = 'Hello'  # on rentre des donnees
s.send(msg) 
keyPubServ=s.recv(2000)
keyPubFileName='clepublicServeur.pub.pem'
pubKeyFile=open(keyPubFileName,"w")
pubKeyFile.write(keyPubServ)
pubKeyFile.close()
                    # Close the socket when done

key_DES='548j75d4'
keyDesFileName='pubDesFile.txt'
keyDesCryptedFileName='pubDesCryptedFile.txt'
pubDesFile=open(keyDesFileName, "w")
pubDesFile.write(key_DES)
pubDesFile.close()
os.system('openssl rsautl -encrypt -in '+keyDesFileName+' -inkey  '+keyPubFileName+' -out '+keyDesCryptedFileName+' -pubin ')


s.send(keyDesCryptedFileName)




s.close 