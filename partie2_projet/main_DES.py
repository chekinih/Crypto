#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:28:32 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""
import DES_cle_64
import DES_cle_112
import DES_cle_168
import os, base64, io, sys

# Fontion qui permet de lire un fichier et de retourner son contenue dans une chaine de caractère
def read_file(path):
    f=io.open(path,mode='r')
    return str(f.read())

# Fonction qui genere une cle de session qui peut etre de 64, 112 ou 168 bits selon 
#le parametre n qui est le nombre de bits de la cle
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
    
plaintext = 'Vous pouvez tester en utilisant les arguments: plaintext key_64 key_112 key_168'
key = '548j75d4'

# recuperer le text a chiffrer soit en ligne de commande soit celui apr defaut est utilise
if (len(sys.argv)>1):
        arg1=str(sys.argv[1])
        if os.path.isfile(arg1):
            plaintext=read_file(arg1)
        else:
           plaintext=arg1 
            
# recuperer les clefs
# Recuperer la clef sur 64 bits
if (len(sys.argv)>2):
        key_64 = str(sys.argv[2])
else: 
    key_64 = generateSecretKey(64)
   
# Recuperer la clef sur 112 bits
if (len(sys.argv)>3):
        key_112 = str(sys.argv[3])
else: 
    key_112 = generateSecretKey(112)
    
# Recuperer la clef sur 168 bits
if (len(sys.argv)>4):
        key_168 = str(sys.argv[4])
else: 
    key_168 = generateSecretKey(168)
    
    
# Execution des trois algos pour chiffrer et dechifrer un messages en utilisant une cle de 64 bits, 112 bits et 168 bits
print("\n")
print("-----------------------------------------Using a 64 bits key-------------------------------------------------------")
print("\n")
print("Text to be crypted: "+ plaintext)
print("\n")
print("key : "+key_64)
print("\n")
cipherText = DES_cle_64.chiffrement_final(plaintext, key_64)
if(cipherText != -1):
    decryptedText = DES_cle_64.dechiffrement_final(cipherText,key_64)
    print("Crypted: "+ decryptedText)
print("\n")  
print("-----------------------------------------Using a 112 bits key-------------------------------------------------------")
print("\n")
print("Text to be crypted: "+ plaintext)
print("\n")
print("key : "+key_112)
print("\n")
cipherText = DES_cle_112.chiffrement_DES_112(plaintext, key_112)
if(cipherText != -1):
    decryptedText = DES_cle_112.dechiffrement_DES_112(cipherText,key_112)
    print("Crypted: "+ decryptedText)
print("\n")
print("-----------------------------------------Using a 168 bits key-------------------------------------------------------")
print("\n")
print("Text to be crypted: "+ plaintext)
print("\n")

print("key : "+key_168)
print("\n")
cipherText = DES_cle_168.chiffrement_DES_168(plaintext, key_168)
if(cipherText != -1):
    decryptedText = DES_cle_168.dechiffrement_DES_168(cipherText,key_168)
    print("Crypted: "+ decryptedText)