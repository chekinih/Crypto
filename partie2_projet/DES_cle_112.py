#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:18:20 2020

@author: user1
"""
import numpy as np
import desComplet

# Transformer la cle en entree en 64 bits
def transform_key_64bits(k):
    k = desComplet.convert_list_to_char(k)
    while(len(k) != 64):
        k = '0' + k 
    return(k)
        
# Separer la cle en entre de taille 112 bits en 2 cles k1 et k2 de taille 64 bits
def separate_in_2_keys_64(k):
    
    # Generer les deux cles k1 et k2 de 56 bits a partir de la cle d entree de 112 bits  
    k1, k2 = desComplet.division(k)
    #print(len(k1))
    # Les cles k1 et k2 sont de taille 56 bits, on va ajouter des 0 au debut pour atteindre 64 bits
    k1 = transform_key_64bits(k1)
    k2 = transform_key_64bits(k2)
    #print(len(k1))
    return k1, k2

def chiffrement_final(text,key):   
    # Transformer le texte a chiffrer en bits
    plaintext_to_binary = desComplet.text_to_bits(text)

    # Transformer le text a chiffrer(qui est en binaire)en un multiple de 64
    while(len(plaintext_to_binary) % 64 != 0):
        plaintext_to_binary = '0' + plaintext_to_binary

    #  Transformer la representation binare du texte a chiffrer en un tableau de caracteres
    plaintext_binary_to_list = desComplet.convert_to_list(plaintext_to_binary)

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

def chiffrement_DES_112(text,key):
    
    if (type(text) != str) :
        print("Le text à chiffrer doit être une chaine de caractères !")
        return -1
    elif (type(key) != str):
        print("La clé doit être une chaine de caractères !")
        return -1
    elif (len(key) != 14):
        print("La clé doit être une chaine de 14 caractères (112 bits) !")
        return -1
    else:
        #print('PlainText avant le chiffrement: '+text)
    
        key_to_binary = desComplet.text_to_bits(key)
        # traiter la cle de 112 bits : 2 clés k1 et k2 de 56bits
        k1, k2 = separate_in_2_keys_64(key_to_binary)
        
        ## Étapes de chiffrages: 
                
        # 1. Partie chiffrage ; chiffrer avec k1
        ciphertext_k1 = chiffrement_final(text, k1)
             
        # 2. Partie chiffrage ; dechiffarge avec k2
        plaintext_k2 = dechiffrement_final(ciphertext_k1, k2)
    
        # 3. Partie chiffrage ; chiffrage avec k1
        ciphertext_e_k1 = chiffrement_final(plaintext_k2, k1)
        return ciphertext_e_k1

def dechiffrement_DES_112(ciphertext,key):
    
    key_to_binary = desComplet.text_to_bits(key)
    # traiter la cle de 112 bits : 2 clés k1 et k2 de 56bits
    k1, k2 = separate_in_2_keys_64(key_to_binary)
    
    ## Étapes de dechiffrage:
        
    # 1. Partie dechiffrage: dechiffrage avec k1
    plaintext_d_k1 = dechiffrement_final(ciphertext, k1)
        
    # 2. Partie dechiffrage: chiffrage avec k2
    ciphertext_d_k2 = chiffrement_final(plaintext_d_k1, k2)
        
    # 3. Partie dechiffage : dechiffrage avec k1
    plaintext_d_k1_ = dechiffrement_final(ciphertext_d_k2, k1)
    return plaintext_d_k1_