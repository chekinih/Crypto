#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 13:50:58 2020

@author: CHEKINI Hakima && BEN SAADA Mariem
"""

from operator import xor
import binascii

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
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

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
def chiffrement(plaintext,key):
    plaintext_to_binary=text_to_bits(plaintext)
    plaintext_binary_to_list=convert_to_list(plaintext_to_binary)
   
    key_to_binary=text_to_bits(key)
    key_binary_to_list=convert_to_list(key_to_binary)
    
    
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
def dechiffrement(ciphertext,key):
    plaintext_binary_to_list=convert_to_list(ciphertext)
    
    key_to_binary=text_to_bits(key)
    key_binary_to_list=convert_to_list(key_to_binary)
    
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
    plaintext=text_from_bits(plaintext_binary)
    return plaintext


def main(text, key):
  
    if (type(text) != str) :
        print("Le text à chiffrer doit être une chaine de caractères !")
        return -1
    elif (len(text) != 8):
        print("Le text à chiffrer doit être une chaine de 8 caractères (64 bits) !")
        return -1
    elif (type(key) != str):
        print("La clé doit être une chaine de caractères !")
        return -1
    elif (len(key) != 8):
        print("La clé doit être une chaine de 8 caractères (64 bits) !")
        return -1
    else:
        print 'PlainText avant le chiffrement: ',text
        
        ciphertext = chiffrement(text, key)
        plaintext = dechiffrement(ciphertext, key)
        print 'PlainText apres le dechiffrement: ',plaintext
        
        if(text == plaintext):
            print("Chiffrement et dechiffrement reussi avec la cle: ", key,"XD !")
            return 0
        else:
            print("Chiffrement et dechiffrement non reussi avec la cle: ", key," X( !")
            return -2
  

print("")
print("----------------------------------Test1--------------------------------------")
res = main('Bonjour!', '12345678')

print("")
print("----------------------------------Test2--------------------------------------")
res = main('Bonjour!', 'F9sGnd4$')


print("")
print("----------------------------------Test3--------------------------------------")
res = main('Bon', 'F9sGnd4$')
print("")
print("----------------------------------Test4--------------------------------------")
res = main([1,2], 'F9sGnd4$')
print("")
print("----------------------------------Test5--------------------------------------")
res = main(['b','n'], 'F9sGnd4$')
print("")
print("----------------------------------Test6--------------------------------------")
res = main(12354678, 'F9sGnd4$')
print("")
print("----------------------------------Test7--------------------------------------")
res = main('Bonjour!', 'F9s')
print("")
print("----------------------------------Test8--------------------------------------")
res = main('Bonjour!', ['b','n','t'])
print("")
print("----------------------------------Test9--------------------------------------")
res = main('Bonjour!', [1,2,3])
print("")
print("----------------------------------Test8--------------------------------------")
res = main('Bonjour!', 54847525)


