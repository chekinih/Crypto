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

plaintext= 'Meriam Hakima'
key='dkkf4'
salt='abdc423cabd23a54'

# passage du plaintext,plaintext et le salt en argument 
# Recuperer le plaintext
if (len(sys.argv)>1):
        plaintext=str(sys.argv[1])
# recuperer la clef
if (len(sys.argv)>2):
        key=str(sys.argv[2])
# recuperer le salt
if (len(sys.argv)>3):
        salt=str(sys.argv[3])

def get_key(password, salt, klen=32, ilen=16, msgdgst='md5'):

    mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
    password = password.encode('ascii', 'ignore')  # convert to ASCII

    try:
        maxlen = klen + ilen
        key_ = mdf(password + salt).digest()
        tmp = [key_]
        while len(tmp) < maxlen:
            tmp.append( mdf(tmp[-1] + password + salt).digest() )
            key_ += tmp[-1]  # append the last byte
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


#print ("\nCipher (CBC) - Base64:\t"+base64.b64encode(ctext))
#print ("\nCipher (CBC) - Hex:\t"+ctext.encode('hex'))
#print ("Cipher in binary:\t",ctext)

plaintext = decrypt(ciphertext,key,AES.MODE_ECB,salt)
plaintext = Padding.removePadding(plaintext,mode='CMS')
print ("\nDecrypted:\t"+plaintext)

c= os.system('ls -l > t.txt')


