#!/usr/bin/python          

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:48:46 2020

@author: CHEKINI Hakima && BEN Saada meriam
"""

#!/usr/bin/python                # This is serveur.py file


import socket                   # Importerle module socket 
import os
import io
#import DES_cle_64
#import DES_cle_112
import DES_cle_168

cleValide='Valide'
cleInvalide='Fin'

# Fontion qui permet de lire un fichier et de retourner son contenue dans une chaine de caractere
def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())

# Cette fonction renvoie vrai si le message en parametre vaut "Valide", faux s il vaut "Fin"
def test_valide(msg):
    if(msg == cleInvalide):
        return False
    if (msg == cleValide):
        return True
    
#Definition des noms des fichiers des cles
keyPrvFileName='clePrive.pem'
keyPubFileName='clepublic.pub.pem'
keyPrvCryptedFileName='clesPriveeChiffree.pem'

#generer une cle privee avec openssl
os.system('openssl genrsa -out '+keyPrvFileName+'  2048')  

 #generer une cle publique avec openssl
os.system('openssl rsa -in '+keyPrvFileName+' -pubout -out '+keyPubFileName)  

#chiffrer la cle privee
os.system('openssl rsa -in '+keyPrvFileName+' -des3 -out '+keyPrvCryptedFileName) 
keyPub=read_file('clepublic.pub.pem')


s = socket.socket()                 # Creer un object socket
host = socket.gethostname()         # Recuperer le nom de la machine locale
port = 1234                         # Reserver un port
s.bind((host, port))                # Faire la liaison avec le port
s.listen(10)                        # Attendre la connexion du client.
while True:
   client, addr = s.accept()        # Etablir la connexion avec le client
   print('Connexion avec ', addr)
   client.send(cleValide)
   recu=client.recv(2000)
   test = test_valide(recu)        # Tester si le client invalide la cle
   if(not test):
       client.close
       print('Fin')
       break
   else:
       
       print ('\nSession '+recu)
       # Le serveur recoit le hello du client
       RequeteDuClient = client.recv(2000) 
       print("J'ai recu "+RequeteDuClient+ " de la part du client\n")
       
       # Envoie de la cle public au client
       print("J'envoie ma cle publique au client")
       client.send(keyPub)
       
       # Recevoir la cle secrete DES du client chiffree
       keyDesCryptedFileName=client.recv(2000)
       print("j'ai recu la cle DES chiffree du client\n")
       
       # dechiffrer la cle DES chiffrer avec la cle secret du serveur
       keyDesDecryptedFileName='pubDesDecryptedFile.txt'
       os.system('openssl rsautl -decrypt -in '+keyDesCryptedFileName+' -inkey  '+keyPrvCryptedFileName+' -out '+keyDesDecryptedFileName)
       print("\nJe dechiffre la cle secrete DES recue")
       keyDESDecryptted = read_file(keyDesDecryptedFileName)
       print("La cle DES du client est: "+ keyDESDecryptted)
       
       # Le serveur repond au client avec un message d acquittement
       print("\nJ'envoie un acquittement au client")
       client.send('ACK')
       
       # Recevoir le message crypte du client
       cryptedMessage = client.recv(2000)
       print("\nJ'ai recu le message chiffre, je vais le dechiffrer")
       #decryptedMessage = DES_cle_64.dechiffrement_final(cryptedMessage,keyDESDecryptted)
       #decryptedMessage = DES_cle_112.dechiffrement_DES_112(cryptedMessage,keyDESDecryptted)
       decryptedMessage = DES_cle_168.dechiffrement_DES_168(cryptedMessage,keyDESDecryptted)
       print("Message dechiffre: "+decryptedMessage)
       
       # Le serveur tente d envoyer lui aussi un message
       print("\nJ'envoie au client un message crypte")
       #cryptedMessage = DES_cle_64.chiffrement_final("Hi there client, i m fine thanks", keyDESDecryptted)
       #cryptedMessage = DES_cle_112.chiffrement_DES_112("Hi there client, i m fine thanks", keyDESDecryptted)
       cryptedMessage = DES_cle_168.chiffrement_DES_168("I am fine client, thanks for asking. If i am answering to you, then your program do the right thing. Bye.", keyDESDecryptted)
       client.send(cryptedMessage)
       
       # Reception du message du client disant que la cle est invalide
       recu1=client.recv(2000)
       test = test_valide(recu1)
       if(not test):
           client.send(cleInvalide)
           client.close
           print('\nFin')
           break
       # Si le client n envoie plus de requetes, le serveur arrete d ecouter
       if not client.recv(2000): 
           break # on break la boucle (sinon les bips vont se repeter)
           
