#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:48:46 2020

@author: CHEKINI Hakima && BEN Saada meriam
"""

#!/usr/bin/python           # This is client.py file

import socket               # Importer le module socket 

import os, base64
import io
#import DES_cle_64
#import DES_cle_112
import DES_cle_168

cleValide='Valide'
cleInvalide='Fin'

# Fontion qui permet de lire un fichier et de retourner son contenue dans une chaine de caractère
def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())


# Fonction qui genere une cle de session qui peut etre de 64, 112 ou 168 bits selon le parametre n qui est le nombre de bits de la cle
def generateSecretKey(n):
    n_octets =  n/8
    if n_octets == 8:
        return  base64.b64encode(os.urandom(5))
    elif n_octets == 14:
        key = base64.b64encode(os.urandom(10))
        key14 = ""
        for i in range (0, n_octets):
            key14 += key[i]
        return key14
    else:
        key = base64.b64encode(os.urandom(16))
        key21 = ""
        for i in range (0, n_octets):
            key21 += key[i]
        return key21

# Cette fonction renvoie vrai si le message en parametre vaut "Valide", faux s il vaut "Fin"
def test_valide(msg):
    if(msg == cleInvalide):
        return False
    if (msg == cleValide):
        return True

s = socket.socket()                 # Creer un object socket
host = socket.gethostname()         # Recuperer le nom de la machine locale
port = 1234                         # Reserver un port

s.connect((host, port))
recu=s.recv(2000)
test = test_valide(recu)            # Tester si la session est valide
if(not test):
    s.send(cleInvalide)
    print('Fin')
    s.close
else:
    print('Session '+recu)
    s.send(cleValide)
    msg = 'Hello'                   # Envoie de message de debut de session
    s.send(msg) 
    
    # rcevoir la cle public du serveur
    keyPubServ=s.recv(2000)
    keyPubFileName='clepublicServeur.pub.pem'
    pubKeyFile=open(keyPubFileName,"w")
    pubKeyFile.write(keyPubServ)
    pubKeyFile.close()
    print("\nJ'ai recu la cle publique du seveur")
                      
    # generation de la cle secrete DES, A decommenter si besoin de voir le resultat en utilisant des cles de 64 bits, 112 bits ou 168 bits
    print("\nJe genere une cle secrete DES")
    #key_DES=generateSecretKey(64)
    #key_DES=generateSecretKey(112)
    key_DES=generateSecretKey(168)
    
    # Mettre la cle des generee dans un fichier 
    keyDesFileName='pubDesFile.txt'
    keyDesCryptedFileName='pubDesCryptedFile.txt'
    pubDesFile=open(keyDesFileName, "w")
    pubDesFile.write(key_DES)
    pubDesFile.close()
    
    # crypter la cle des secrete genere par le client avec la cle publique du serveur recue
    os.system('openssl rsautl -encrypt -in '+keyDesFileName+' -inkey  '+keyPubFileName+' -out '+keyDesCryptedFileName+' -pubin ')

    print("J'envoie la cle DES cryptee\n")
    # Envoie de la cle secrete chiffree
    s.send(keyDesCryptedFileName)
    
    # Recevoir l'acquittement du serveur
    acquittementServeur=s.recv(2000)
    if(acquittementServeur == "ACK"):
        print(acquittementServeur +" :Acquittement recu de la part du serveur")
        
        # Envoie d un message crypte au serveur
        print("\nJ'envoie au serveur un message crypte")
        #cryptedMessage = DES_cle_64.chiffrement_final("HELLO SERVER, HOW ARE YOU!", key_DES)
        #cryptedMessage = DES_cle_112.chiffrement_DES_112("HELLO SERVER, HOW ARE YOU!", key_DES)
        cryptedMessage = DES_cle_168.chiffrement_DES_168("How are you server? this message is just to test if our program do the right thing. Take care, see You soon.", key_DES)
        s.send(cryptedMessage)
        
        # Recevoir le message chiffre du serveur
        cryptedMessage = s.recv(2000)
        print("\nJ'ai recu le message chiffre, je vais le dechiffrer")
        #decryptedMessage = DES_cle_64.dechiffrement_final(cryptedMessage,key_DES)
        #decryptedMessage = DES_cle_112.dechiffrement_DES_112(cryptedMessage,key_DES)
        decryptedMessage = DES_cle_168.dechiffrement_DES_168(cryptedMessage,key_DES)
        print("Message dechiffre: "+decryptedMessage)

        # Le client invalide la cle
        s.send(cleInvalide)
        recu1=s.recv(2000)
        test = test_valide(recu1)
        if(not test):
            print('\nFin')
            s.close
        
   
   