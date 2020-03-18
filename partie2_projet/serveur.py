#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import os
import io
import TP1


def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())

keyPrvFileName='clePrive.pem'
keyPubFileName='clepublic.pub.pem'
keyPrvCryptedFileName='clesPriveeChiffree.pem'
os.system('openssl genrsa -out '+keyPrvFileName+'  2048')  #generer une cle privee avec openssl
os.system('openssl rsa -in '+keyPrvFileName+' -pubout -out '+keyPubFileName)   #generer une cle publique avec openssl
os.system('openssl rsa -in '+keyPrvFileName+' -des3 -out '+keyPrvCryptedFileName) #chiffrer la cle privee
keyPub=read_file('clepublic.pub.pem')


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1234          # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(10)                 # Now wait for client connection.
while True:
   client, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   client.send('Thank you for connecting')
   # le serveur recoit le hello du client
   RequeteDuClient = client.recv(2000) # on recoit 255 caracteres grand max
   if not RequeteDuClient: # si on ne recoit plus rien
       break  # on break la boucle (sinon les bips vont se repeter)
   print (RequeteDuClient,"\a")
   # envoie de la cle public au client
   print("j'envoie ma cle publique au client")
   client.send(keyPub)
   # Recevoir la cle secrete des du client chiffree
   keyDesCryptedFileName=client.recv(2000)
   print("j'ai recu la cle des chiffree du client")
   keyDesDecryptedFileName='pubDesDecryptedFile.txt'
   # dechiffrer la cle DES chiffrer avec la cle secret du serveur
   os.system('openssl rsautl -decrypt -in '+keyDesCryptedFileName+' -inkey  '+keyPrvCryptedFileName+' -out '+keyDesDecryptedFileName)
   print("je dechiffre la cle secrete DES recu")
   keyDESDecryptted = read_file(keyDesDecryptedFileName)
   print("La cle DES du client est: "+ keyDESDecryptted)
   # Le serveur repond au client avec un message d acquittement
   print("j'envoie un acquittement au client")
   client.send('serveur => client : Cle DES recu')
   
   # Recevoir le message chiffre du client
   cryptedMessage = client.recv(2000)
   print("J ai recu le message chiffre, je vais le dechiffrer")
   decryptedMessage = TP1.dechiffrement_final(cryptedMessage,keyDESDecryptted)
   print("Message dechiffre: "+decryptedMessage)
   
   
   # Le serveur tente d envoyer lui aussi un message
   print("J envoie au client un message crypte")
   cryptedMessage = TP1.chiffrement_final("Hi there client, i m fine thanks", keyDESDecryptted)
   client.send(cryptedMessage)
   
   # Reception du message du client disant que la cle est invalide
   cleInvalide = client.recv(2000)
   print(cleInvalide)
   
   # Le serveur invalide la cle
   client.send("j'invalide la cle")
   
   # Si le client n envoie plus de requetes, le serveur arrete d ecouter
   if not client.recv(2000):
       break
   client.close()                # Close the connection
