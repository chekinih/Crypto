#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 13:50:58 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""

from operator import xor
import binascii
import numpy as np
import sys

# les S-box
s1=[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]

s2=[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
    [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
    [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
    [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]

s3=[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
    [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
    [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
    [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]

s4=[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
    [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
    [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
    [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]

s5=[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
    [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
    [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
    [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]

s6=[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
    [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
    [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
    [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]

s7=[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
    [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
    [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
    [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]

s8=[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
    [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
    [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
    [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]


# convertir une chaine de caractere en sa valeur binaire ascii
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Convertir un ascii en sa valeur en octet
def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# Convertir des bits en une chaine de caracteres
def text_from_bits(bits, encoding='utf-8'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding)

# COnvertir une chaine de caractere en une liste de caracteres
def convert_to_list(str):

  string_length = len(str)
  tab = []
  for i in range(0, string_length):
    tab.append(str[i])
  return tab;

# COnvertir une  liste de caracteres en une chaine de caracteres
def convert_list_to_char(lst):
    ch=''
    for i in range(0,len(lst)):
        ch=ch+lst[i]
    return ch

# Convertir un tableau de caracteres compose de 0 et 1 (valeur binaire) en sa valeur en decimal
def conversion_to_decimal(x):
    res = 0
    for i in range(0, len(x)):
        if(x[i] == '1'):
            res += pow(2,len(x)-i-1)

    return res

# Convertir un decimal en sa valeur en binaire sur quatre bits
def conversion_to_binary(decimal):
    tab = []
    while True:
        if(decimal/2 != 0):
            tab.append(decimal % 2)
            decimal = decimal / 2
        else:
            tab.append(decimal % 2)
            break
    #pour coder le decimal sur 4 bits
    while (len(tab)<4):
        tab.append(0)

    reverse_tab = []
    for i in reversed(tab):
        reverse_tab.append(str(i))
    return reverse_tab

# Calculer le xor entre deux tableaux x1 et x2
def logical_xor(x1, x2):
    tab = []
    for i in range(0, len(x1)):
        if(x1[i] == x2[i]):
            tab.append('0')
        else:
            tab.append('1')
    return tab

# Effectuer l operation xor sur le resultat de EP(8 bits) et la clef K1
def xor_EP_K(res_EP, k):
    return logical_xor(res_EP, k)

# Diviser un tableau en deux left et right
def division(param):
    left_half = []
    right_half = []
    for i in range(0, len(param)):
        if(i < len(param)/2):
            left_half.append(param[i])
        else:
            right_half.append(param[i])

    return left_half, right_half

# Transformer la cle en entree en 64 bits
def transform_key_64bits(k):
    k = convert_list_to_char(k)
    while(len(k) != 64):
        k = '0' + k 
    return(k)
        
# Separer la cle en entre de taille 112 bits en 2 cles k1 et k2 de taille 64 bits
def separate_in_2_keys_64(k):
    
    # Generer les deux cles k1 et k2 de 56 bits a partir de la cle d entree de 112 bits  
    k1, k2 = division(k)
    
    # Les cles k1 et k2 sont de taille 56 bits, on va ajouter des 0 au debut pour atteindre 64 bits
    k1 = transform_key_64bits(k1)
    k2 = transform_key_64bits(k2)
    return k1, k2
    
# permutation generale
# lst : un tableau d entree
# index :  un tableau des index depend de la permutation souhaite
def General_Permutation(lst,index):
    tab = []
    for i in range(0,len(index)):
        tab.append(lst[index[i]])
    return tab

#Permutation Initiale
def IP(lst):
    index_IP=[57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,
              15,7,56,48,40,32,24,16,8,0,58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6]
    return General_Permutation(lst,index_IP)

#Permutation Finale: inverse de IP
def FP(lst):
     index_FP=[39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,
               43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25,32,0,40,8,48,16,56,24]
     return General_Permutation(lst,index_FP)

#Permutation Choice One
def PC1(lst):
    index_PC1=[56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,
               22,14,6,61,53,45,37,29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]
    return General_Permutation(lst,index_PC1)

#Permutation Choice two
def PC2(lst):
    index_PC2=[13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,
               32,47,43,48,38,55,33,52,45,41,49,35,28,31]
    return General_Permutation(lst,index_PC2)

#Expansion Permutation
def EP(lst):
    index_EP=[31,0,1,2,3,4,3,4,5,6,7,8,7,8,9,10,11,12,11,12,13,14,15,16,15,16,17,18,19,20,19,20,21,22,23,24,
              23,24,25,26,27,28,27,28,29,30,31,0]
    return General_Permutation(lst,index_EP)

#Permuation Function
def Permutation_Func(lst):
    index_P=[15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]
    return General_Permutation(lst,index_P)

# Rotation a gauche d un seul bit
def LS_1_Bit(half_permuted_key):
    tab = []
    tab_length = len(half_permuted_key)
    for i in range(0, tab_length-1):
        tab.append(half_permuted_key[i+1])
    tab.append(half_permuted_key[0])
    return tab

# Rotation a gauche de 2 bit
# Pour trouver LS_2_Bit, il faut appliquer 2 fois LS_1_Bit sur half_permuted_key
def LS_2_Bit(half_permuted_key):
    return LS_1_Bit(LS_1_Bit(half_permuted_key))

# Concatener deux tableaux
def concat_ls_keys(left, right):
    tab = []
    tab = left + right
    return tab

# Generer les 16 cles a partir d une cles de 64 bits
def generate_keys(key):
    tab_keys = []
    permuted_pc1 = PC1(key)
    left_pc1, right_pc1 = division(permuted_pc1)
    left = left_pc1
    right = right_pc1
    for i in range(1,17):
        if(i == 1 or i == 2 or i==9 or i==16):
            left_prec= left
            right_prec = right
            left = LS_1_Bit(left_prec)
            right = LS_1_Bit(right_prec)
        else:
            left = LS_2_Bit(left_prec)
            right = LS_2_Bit(right_prec)

        concat_ls_k = concat_ls_keys(left, right)
        k = PC2(concat_ls_k)
        tab_keys.append(k)
    return tab_keys

# La fonction F qui fait le EP, XOR avc la cle ki, subtitution choice(s-box) et la fonction de permutation
def F(right_half, k):
    res_EP = EP(right_half)
    #print 'ep', res_EP
    res_xor_EP_K = xor_EP_K(res_EP, k)

    s_box=[s1,s2,s3,s4,s5,s6,s7,s8]
    count=0
    i=0
    binary_res_s=[]
    while (count<len(res_xor_EP_K )):

        #print 'res_xor_EP_K1',res_xor_EP_K1
        line_s = conversion_to_decimal([res_xor_EP_K[0+count], res_xor_EP_K[5+count]])
        #print 'line_s0',line_s0
        column_s = conversion_to_decimal([res_xor_EP_K[1+count], res_xor_EP_K[4+count]])
        #print 'column_s0',column_s0
        s=s_box[i]
        res_S = s[line_s][column_s]
        #print 'res_S0',res_S0
        binary_res_s = binary_res_s + conversion_to_binary(res_S)
        #print binary_res_s , len(binary_res_s)
        count=count+6
        i=i+1
    #print("binary_res_s",len(binary_res_s))
    permut_func = Permutation_Func(binary_res_s)
    #print("permut_func",len(permut_func))
    return permut_func

# fk fait le xor du resultat du F avec la partie gauche du resultat precedent
def fk(res_prec, k):
    left, right = division(res_prec)
    res_F = F(right, k )
    return logical_xor(left,res_F )

# Switch qui inverse les deux parties gauche et doite
def SW(res_fk_prec, right_prec):
    return right_prec + res_fk_prec

# Chiffrer un plaintext (chaine de caractere de 8 bits) avec la cle k(chaine de caractere de 8 bits)
def chiffrement(plaintext_binary_to_list,key):

    key_to_binary = text_to_bits(key)
    key_binary_to_list = convert_to_list(key_to_binary)

    key_table= generate_keys(key_binary_to_list)
    res_IP=IP(plaintext_binary_to_list)
    res_prec=res_IP

    for i in range (0,16):
        left_prec,right_prec=division(res_prec)
        res_fk=fk(res_prec,key_table[i])
        res_sw=SW(res_fk,right_prec)
        res_prec=res_sw

    left_res,right_res=division(res_prec)
    res=SW(left_res,right_res)
    ciphertext_list=FP(res)

    # Conversion de la liste des caracteres en une chaine de caracteres
    ciphertext = convert_list_to_char(ciphertext_list)
    return ciphertext


# Dechiffrer un ciphertext (resultat du chiffrement de plaintext) avec la cle k
def dechiffrement(plaintext_binary_to_list,key):

    #key_to_binary=text_to_bits(key)
    key_binary_to_list=convert_to_list(key)
    key_table= generate_keys(key_binary_to_list)
    res_IP=IP(plaintext_binary_to_list)
    res_prec=res_IP
    
    i=15
    while i>=0:
        left_prec,right_prec=division(res_prec)
        res_fk=fk(res_prec,key_table[i])
        res_sw=SW(res_fk,right_prec)
        res_prec=res_sw
        i-=1

    left_res,right_res=division(res_prec)
    res=SW(left_res,right_res)
    plaintext_list=FP(res)

    # Conversion de la liste des caracteres en une chaine de caracteres
    plaintext_binary = convert_list_to_char(plaintext_list)
    #print(len(plaintext_binary))    == >64
    #plaintext=text_from_bits(plaintext_binary)
    return plaintext_binary


def main(text, key):
    # Transformer le texte a chiffrer en bits
    plaintext_to_binary = text_to_bits(text)

    # Transformer le text a chiffrer(qui est en binaire)en un multiple de 64
    while(len(plaintext_to_binary) % 64 != 0):
        plaintext_to_binary = '0' + plaintext_to_binary

    #  Transformer la representation binare du texte a chiffrer en un tableau de caracteres
    plaintext_binary_to_list = convert_to_list(plaintext_to_binary)

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
        print('PlainText avant le chiffrement: ',text)
    
        print(text_to_bits(text))
        # traiter la cle de 112 bits : 2 clés k1 et k2 de 56bits
        # les etapes pour le chiffrement: 
        # 1. Chiffrer avec k1
        # 2. Déchiffrer avec k2
        # 3. Chiffrer avec k1
        

        key_to_binary = text_to_bits(key)
        #print(key_to_binary)
        k1, k2 = separate_in_2_keys_64(key_to_binary)
        #print(k2)  ==> bunaire chaine caractere
        # Separer en blocs de 64 bits pour cryptage
        blocs_binary_plaintext = np.array_split(plaintext_binary_to_list,len(plaintext_binary_to_list)/64 )
        # Chiffrage du message par blocs de 64 bits
        ciphertext = ""
        for i in range(0, len(blocs_binary_plaintext)):
            ciphertext += chiffrement(blocs_binary_plaintext[i], k1)
        #print(type(ciphertext)) => str
        
        # Convertir le texte chiffre en une liste
        ciphertext_binary_to_list = convert_to_list(ciphertext)
        #  Separer en blocs de 64 bits pour decryptage
        blocs_binary_ciphertext = np.array_split(ciphertext_binary_to_list,len(ciphertext_binary_to_list)/64 )
        #print (len(blocs_binary_ciphertext)) okok
        
        #print(text_from_bits('0110101001100101011010110110101101101011011010100110101001101010'))
        # Dechiffrage du message crypte par blocs de 64 bits
        plaintext_e_k2= ""
        for i in range(0, len(blocs_binary_ciphertext)):
            plaintext_e_k2 += dechiffrement(blocs_binary_ciphertext[i], k2)
        
        #print(plaintext_e_k2)
        
        
        
         # Transformer le text a chiffrer(qui est en binaire)en un multiple de 64
        while(len(plaintext_e_k2) % 64 != 0):
            plaintext_to_binary = '0' + plaintext_to_binary
        plaintext_binary_to_list = convert_to_list(plaintext_to_binary)
           
        
        # Separer en blocs de 64 bits pour cryptage
        blocs_binary_plaintext = np.array_split(plaintext_binary_to_list,len(plaintext_binary_to_list)/64 )
        # Chiffrage du message par blocs de 64 bits
        ciphertext_c_k1 = ""
        for i in range(0, len(blocs_binary_plaintext)):
            ciphertext_c_k1 += chiffrement(blocs_binary_plaintext[i], k1)
            
       # print(ciphertext_c_k1)
            
            
       
       # partie dechiffrement
       
       # Transformer le text a chiffrer(qui est en binaire)en un multiple de 64
        while(len(ciphertext_c_k1) % 64 != 0):
            ciphertext_c_k1 = '0' + ciphertext_c_k1
        ciphertext_binary_to_list = convert_to_list(ciphertext_c_k1)
        
        # Separer en blocs de 64 bits pour cryptage
        blocs_binary_ciphertext_d_k1 = np.array_split(ciphertext_binary_to_list,len(ciphertext_binary_to_list)/64 )
        # Chiffrage du message par blocs de 64 bits
        ciphertext_d_k1 = ""
        for i in range(0, len(blocs_binary_ciphertext_d_k1)):
            ciphertext_d_k1 += dechiffrement(blocs_binary_ciphertext_d_k1[i], k1)
            
        
        
         # dechiffrement avec k2 pour la partie dechiffrement
        
        # Convertir le texte chiffre en une liste
        ciphertext_binary_to_list_d_k2 = convert_to_list(ciphertext_d_k1)
        #  Separer en blocs de 64 bits pour decryptage
        blocs_binary_ciphertext_d_k2 = np.array_split(ciphertext_binary_to_list_d_k2,len(ciphertext_binary_to_list_d_k2)/64 )
 
        # Dechiffrage du message crypte par blocs de 64 bits
        plaintext_d_k2 = ""
        for i in range(0, len(blocs_binary_ciphertext_d_k2)):
            plaintext_d_k2 += chiffrement(blocs_binary_ciphertext_d_k2[i], k2)
           
        
        # Chiffrement avec k1 pour la partie dechiffrement
        
        
        #  Transformer la representation binare du texte a chiffrer en un tableau de caracteres
        plaintext_binary_to_list_d_k1 = convert_to_list(plaintext_d_k2)
        
        # Separer en blocs de 64 bits pour cryptage
        blocs_binary_plaintext_d_k1 = np.array_split(plaintext_binary_to_list_d_k1,len(plaintext_binary_to_list_d_k1)/64 )
        # Chiffrage du message par blocs de 64 bits
        ciphertext_d_k1_ = ""
        for i in range(0, len(blocs_binary_plaintext_d_k1)):
            ciphertext_d_k1_ += dechiffrement(blocs_binary_plaintext_d_k1[i], k1)
        
        print((ciphertext_d_k1_))
        
        
        #print(plaintext_e_k1)
        # peut etre faire une fonction pour ce petit bloc 
        
       #ici
       
       
       #ici
        #('0011101001010010111010001011010111111101101000001111110011011
                             #'100100110101000010100101011110100100101111110111011010000010001010101101
                             #'0011111100111101000010111000111110101010000010010001111011001001101000011
                             #'01111001000011110101000111110101011111100111011101100101110011011110111100
                             #'100100101011001101011101'))
        #print(text_from_bits('00001001'))
        #print(text_from_bits('11010101'))  ==> probleme
        #print(conversion_to_decimal('11010101'))
            
       
            
        #print('PlainText apres le dechiffrement: ',ciphertext)


        #if(text == ciphertext):
            #print("Chiffrement et dechiffrement reussi avec la cle: "+key+" XD !")
            #return 0
        #else:
            #print("Chiffrement et dechiffrement non reussi avec la cle: "+ key +" X( !")
            #return -2

res = main('je', '11111125235415')