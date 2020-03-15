#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:31:49 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""

import os
import io
import sys

# methode qui permet de lire un fichier et retourne son contenu
def read_file(path):
    f=io.open(path,mode='r')
    content=str(f.read())
    f.close()
    return content

# methode qui permet d ecrire un contenu dans un fichier
def write_file(path,content):
    f=open(path, "w")
    f.write(content)
    f.close()

# methode qui genere une cle privee avec la commande rsa de openssl
def generate_private_key():
    keyPrvFileName='clePriveTp2.pem'
    os.system('openssl genrsa -out '+keyPrvFileName+'  2048')
    return keyPrvFileName

# methode qui genere une cle publique avec la commande rsa de openssl 
# et prend en arguments le path du fichier contenant la cle privee
def generate_public_key(keyPrvFileName):
    keyPubFileName='clePublicTp2.pub.pem'
    os.system('openssl rsa -in '+keyPrvFileName+' -pubout -out '+keyPubFileName)
    return keyPubFileName

# methode qui chiffre la cle privee rsa avec un algorithme symetrique (des3)
def encrypt_private_key(keyPrvFileName):
    keyPrvCryptedFileName='clesPriveeChiffreeTp2.pem'
    os.system('openssl rsa -in '+keyPrvFileName+' -des3 -out '+keyPrvCryptedFileName)
    return keyPrvCryptedFileName

# methode qui chiffre un plaintext avec la cle publique
#plaintextFileName est le nom d un fichier txt contenant le plaintext a chiffrer
def encrypt_plaintext(plaintextFileName,keyPubFileName):
    ciphertextFileName='ciphertextFileNameTp2.txt'
    os.system('openssl rsautl -encrypt -in '+plaintextFileName+' -inkey  '+keyPubFileName+' -out '+ciphertextFileName+' -pubin ')
    return ciphertextFileName

# methode qui dechiffre un ciphertext avec la cle privee
#ciphertextFileName est le nom d un fichier txt contenant le ciphertext a dechiffrer
def decrypt_ciphertext(ciphertextFileName,keyPrvCryptedFileName):
    cryptedTextFileName='cryptedTextFileNameTp2.txt'
    os.system('openssl rsautl -decrypt -in '+ciphertextFileName+' -inkey  '+keyPrvCryptedFileName+' -out '+cryptedTextFileName)
    return cryptedTextFileName

# methode qui permet de faire un scenario de test : generer les cles et faire un chiffrement et un dechiffrement 
# cette methode prend en parametre un plaintext    
def main(plainttext):
    plaintextFileName='plaintextFileNameTp2.txt'
    plaintextFile=open(plaintextFileName, "w")
    plaintextFile.write(plainttext)
    plaintextFile.close()
    
    keyPrvFileName=generate_private_key()
    keyPubFileName=generate_public_key(keyPrvFileName)
    keyPrvCryptedFileName=encrypt_private_key(keyPrvFileName)
    ciphertextFileName=encrypt_plaintext(plaintextFileName,keyPubFileName)
    cryptedTextFileName=decrypt_ciphertext(ciphertextFileName,keyPrvCryptedFileName)
    ciphertextFile=io.open(cryptedTextFileName,mode='r')
    ciphertext=str(ciphertextFile.read())
    ciphertextFile.close()
    
    print('\nplaintext :\t '+plainttext)
    print ("\nDecrypted:\t"+ciphertext)
    return ciphertext


# le plaintext peut etre passe en argument sous la forme d une chaine de caractere ou bien un path d un fichier qui contient le plaintext
# si le plaintext n est pas passe en argument on prend le plaintext definit par defaut
plaintext='vous pouvez tester en passant le plaintext en arguments'
if (len(sys.argv)>1):
        arg1=str(sys.argv[1])
        if os.path.isfile(arg1):
            plaintext=read_file(arg1)
        else:
           plaintext=arg1
           
main(plaintext)
