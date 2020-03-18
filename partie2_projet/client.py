#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:48:46 2020

@author: 11607156
"""

#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

import os, base64
import io
import TP1

def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())

# Fonction qui genere une cle de session de 64 bits
def generateSecretKey():
    return base64.b64encode(os.urandom(5))

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1234               # Reserve a port for your service.

s.connect((host, port))
print (s.recv(1024))
msg = 'Hello'  # on rentre des donnees
s.send(msg) 
# rcevoir la cle public du serveur
keyPubServ=s.recv(2000)
keyPubFileName='clepublicServeur.pub.pem'
pubKeyFile=open(keyPubFileName,"w")
pubKeyFile.write(keyPubServ)
pubKeyFile.close()
print("J'ai reçu la clé publique du seveur")
                    # Close the socket when done
print("Je genere une cle secrete des")
key_DES=generateSecretKey()
keyDesFileName='pubDesFile.txt'
keyDesCryptedFileName='pubDesCryptedFile.txt'
pubDesFile=open(keyDesFileName, "w")
# Mettre la cle des generee dans un fichier 
pubDesFile.write(key_DES)
pubDesFile.close()
# crypter la cle des secrete genere par le client avec la cle publique du serveur recue
os.system('openssl rsautl -encrypt -in '+keyDesFileName+' -inkey  '+keyPubFileName+' -out '+keyDesCryptedFileName+' -pubin ')
#
print("j'envoie la cle des cryptee")
# Envoie de la cle secrete chiffree
s.send(keyDesCryptedFileName)
acquittementServeur=s.recv(2000)
print(acquittementServeur)
print("Acquittement recu de la part du serveur")

# Envoie d un message crypte au serveur
print("J envoie au serveur un message crypte")
cryptedMessage = TP1.chiffrement_final("HELLO SERVER, HOW ARE YOU!", key_DES)
s.send(cryptedMessage)

# Recevoir le message chiffre du serveur
cryptedMessage = s.recv(2000)
print("J ai recu le message chiffre, je vais le dechiffrer")
decryptedMessage = TP1.dechiffrement_final(cryptedMessage,key_DES)
print("Message dechiffre: "+decryptedMessage)

# Le client invalide la cle
s.send("j'invalide la cle")

# Reception du message du client disant que la cle est invalide
cleInvalide = s.recv(2000)
print(cleInvalide)
s.close 