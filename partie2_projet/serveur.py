#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import os
import io


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
   print 'Got connection from', addr
   client.send('Thank you for connecting')
   RequeteDuClient = client.recv(2000) # on recoit 255 caracteres grand max
   if not RequeteDuClient: # si on ne recoit plus rien
       break  # on break la boucle (sinon les bips vont se repeter)
   print RequeteDuClient,"\a" 
   client.send(keyPub)
   
   keyDesCryptedFileName=client.recv(2000)
   keyDesDecryptedFileName='pubDesDecryptedFile.txt'
   os.system('openssl rsautl -decrypt -in '+keyDesCryptedFileName+' -inkey  '+keyPrvCryptedFileName+' -out '+keyDesDecryptedFileName)
   
   client.close()                # Close the connection
