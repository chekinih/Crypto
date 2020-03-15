#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:31:49 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""

from Crypto.Cipher import AES
import sys
import base64
import Padding
import os
import io

# methode qui permet de lire un fichier et retourne son contenu
def read_file(path):
    f=io.open(path,mode='r')
    content=str(f.read())
    f.close()
    return content

plaintext= 'Meriam Hakima'
key='dkkf4'
salt='abdc423cabd23a54'

# passage du plaintext,plaintext et le salt en argument 
# Recuperer le plaintext
# le plaintext peut etre passe en argument sous la forme dans chaine de caractere ou bien un path d un fichier qui contient le plaintext
# si le plaintext n est pas passe en argument en prend le plaintext definit par defaut
if (len(sys.argv)>1):
        arg1=str(sys.argv[1])
        if os.path.isfile(arg1):
            plaintext=read_file(arg1)
        else:
           plaintext=arg1
# recuperer la clef
# la clef peut etre passe en argument sous la forme dans chaine de caractere ou bien un path d un fichier qui contient la clef
# si la clef n est pas passe en argument en prend la clef definit par defaut
if (len(sys.argv)>2):
        arg2=str(sys.argv[2])
        if os.path.isfile(arg2):
            key=read_file(arg2)
        else:
           key=arg2
# recuperer le salt
# le salt peut etre passe en argument sous la forme dans chaine de caractere ou bien un path d un fichier qui contient le salt
# si le salt n est pas passe en argument en prend le salt definit par defaut
if (len(sys.argv)>3):
        arg3=str(sys.argv[3])
        if os.path.isfile(arg3):
            salt=read_file(arg3)
        else:
           salt=arg3
           
#genererles 2 cles : cle publique et iv
def get_key(password, salt, klen=32, ilen=16, msgdgst='md5'):

    mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
    password = password.encode('ascii', 'ignore')  # convertir en ASCII

    try:
        maxlen = klen + ilen
        key_ = mdf(password + salt).digest()
        tmp = [key_]
        while len(tmp) < maxlen:
            tmp.append( mdf(tmp[-1] + password + salt).digest() )
            key_ += tmp[-1]  # ajouter le dernier octet
        key = key_[:klen]
        
        iv = key_[klen:klen+ilen]
        return key,iv
        
    except UnicodeDecodeError:
         return None, None
     
# fonction qui chiffre le message plaintext
def encrypt(plaintext,key, mode,salt):
    key,iv=get_key(key,salt.decode('hex'))
    encobj = AES.new(key,mode)
    return(encobj.encrypt(plaintext))

# Fonction qui dechiffre le message chiffre
def decrypt(ciphertext,key, mode,salt):
    key,iv=get_key(key,salt.decode('hex'))
    encobj = AES.new(key,mode)
    return(encobj.decrypt(ciphertext))

print ("Plaintext:\t" + plaintext)
print ("Passphrase:\t" + key)
print ("Salt:\t\t"+ salt)

plaintext = Padding.appendPadding(plaintext,mode='CMS')

ciphertext = encrypt(plaintext,key,AES.MODE_ECB,salt)

ctext = b'Salted__' + salt.decode('hex') + ciphertext

plaintext = decrypt(ciphertext,key,AES.MODE_ECB,salt)
plaintext = Padding.removePadding(plaintext,mode='CMS')
print ("\nDecrypted:\t"+plaintext)


