#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:00:22 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""
import numpy as np
import desComplet

# a mettre ici le chiffrement final et dechi final de tp1
# apres faire de meme avec la cle 112 bit
#et l autre cle
#
def chiffrement_final(text,key):   
    # Transformer le texte a chiffrer en bits
    plaintext_to_binary = desComplet.text_to_bits(text)

    # Transformer le text a chiffrer(qui est en binaire)en un multiple de 64
    while(len(plaintext_to_binary) % 64 != 0):
        plaintext_to_binary = '0' + plaintext_to_binary

    #  Transformer la representation binare du texte a chiffrer en un tableau de caracteres
    plaintext_binary_to_list = desComplet.convert_to_list(plaintext_to_binary)

    if (type(text) != str) :
        print("Erreur: Le text à chiffrer doit être une chaine de caractères !")
        return -1
    elif (type(key) != str):
        print("Erreur: La clé doit être une chaine de caractères !")
        return -1
    elif (len(key) != 8):
        print("Erreur: La clé doit être une chaine de 8 caractères (64 bits) !")
        return -1
    else:
        #print('PlainText avant le chiffrement: ',text)

        # Separer en blocs de 64 bits pour cryptage
        blocs_binary_plaintext = np.array_split(plaintext_binary_to_list,len(plaintext_binary_to_list)/64 )
        # Chiffrage du message par blocs de 64 bits
        ciphertext = ""
        for i in range(0, len(blocs_binary_plaintext)):
            ciphertext += desComplet.chiffrement(blocs_binary_plaintext[i], key)
        
    return ciphertext

def dechiffrement_final(ciphertext,key):
    # Convertir le texte chiffre en une liste
    ciphertext_binary_to_list = desComplet.convert_to_list(ciphertext)
    #  Separer en blocs de 64 bits pour decryptage
    blocs_binary_ciphertext = np.array_split(ciphertext_binary_to_list,len(ciphertext_binary_to_list)/64 )
    # Dechiffrage du message crypte par blocs de 64 bits
    plaintext = ""
    for i in range(0, len(blocs_binary_ciphertext)):
        plaintext += desComplet.dechiffrement(blocs_binary_ciphertext[i], key)
    
    #print('PlainText apres le dechiffrement: ',plaintext)
    return plaintext