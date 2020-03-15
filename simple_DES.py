#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: CHEKINI Hakima && BEN SAADA Mariem
"""
from operator import xor
import binascii
import sys

# les S-box
s0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

s1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

# convertir une chaine de caractere en sa valeur binaire ascii
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Convertir un ascii en sa valeur en octet
def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# Convertir un ascii en sa valeur en octet
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

# Convertir un decimal en sa valeur en binaire sur 2 bits
def conversion_to_binary(decimal):
    original_decimal = decimal
    tab = []
    while True:
        if(decimal/2 != 0):
            tab.append(decimal % 2)
            decimal = decimal / 2
        else:
            tab.append(decimal % 2)
            break
    if( original_decimal == 1 or original_decimal == 0):
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

# effectuer l operation xor sur le resultat de EP(8 bits) et la clef K1
def xor_EP_K1(res_EP, k1):
    return logical_xor(res_EP, k1)

# Diviser un tableau passe en parametre en deux left et right
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

# Permutation 10: P10
def permute_10(key):
    index_P10=[2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    return General_Permutation(key,index_P10)

# Permutation P8
def permute_8(key):
    index_P8=[5, 2,6, 3, 7, 4 ,9, 8]
    return General_Permutation(key,index_P8)

# permutation initiale
def IP(plaintext):
    index_IP=[1, 5, 2, 0, 3, 7, 4, 6]
    return General_Permutation(plaintext, index_IP)

# permutation finale (inverse de IP)
def FP(plaintext):
    index_FP=[3, 0, 2, 4, 6, 1, 7, 5]
    return General_Permutation(plaintext, index_FP)

# EP = Expansion/permutation
# utiliser 4 bits de droite du resultat de IP
def EP(half_right_result_IP):
    index_EP=[3,0, 1, 2, 1, 2, 3, 0]
    return General_Permutation(half_right_result_IP, index_EP)

# Permutation P4
def permute_4(res_s0_s1):
    
    index_P4=[1, 3, 2, 0]
    return General_Permutation(res_s0_s1, index_P4)

# Rotation a gauche  d un seul bit
def LS_1(half_permuted_key):
    tab = []
    tab_length = len(half_permuted_key)
    for i in range(0, tab_length-1):
        tab.append(half_permuted_key[i+1])
    tab.append(half_permuted_key[0])
    return tab

# Pour trouver LS_2, il faut appliquer 2 fois LS1 sur
# chaque moitie de la clef apres avoir applique LS1
def LS_2(result_LS1):
    return LS_1(LS_1(result_LS1))

# concatenation des deux demis clefs apres la rotation circulaire a gauche (LS_1 + L_S1)
def concat_ls_keys(left, right):
    tab = []
    tab = left + right
    return tab

# Generer les cles a partir d une cles de 10 bits
def generate_k(key):
    permuted_10 = permute_10(key)
    left, right = division(permuted_10)
    half_left_ls1 = LS_1(left)
    half_right_ls1 = LS_1(right)
    concat_ls_k1 = concat_ls_keys(half_left_ls1, half_right_ls1)
    k1 = permute_8(concat_ls_k1)

    half_left_ls2 = LS_2(half_left_ls1)
    half_right_ls2 = LS_2(half_right_ls1)
    concat_ls_k2 = concat_ls_keys(half_left_ls2, half_right_ls2)
    k2 = permute_8(concat_ls_k2)

    return k1, k2

# La fonction F qui fait le EP, XOR avc la cle ki ...
def F(right_half_IP, k1):
    res_EP = EP(right_half_IP)
    res_xor_EP_K1 = xor_EP_K1(res_EP, k1)
    
    line_s0 = conversion_to_decimal([res_xor_EP_K1[0], res_xor_EP_K1[3]])
    column_s0 = conversion_to_decimal([res_xor_EP_K1[1], res_xor_EP_K1[2]])
    
    res_S0 = s0[line_s0][column_s0]
    binary_res_s0 = conversion_to_binary(res_S0)
   
    line_s1 = conversion_to_decimal([res_xor_EP_K1[4], res_xor_EP_K1[7]])
    column_s1 = conversion_to_decimal([res_xor_EP_K1[5], res_xor_EP_K1[6]])
    res_S1 = s1[line_s1][column_s1]
  
    binary_res_s1 = conversion_to_binary(res_S1)
    p4 = permute_4(binary_res_s0 + binary_res_s1)
    
    return p4
    
# Fonction fk
def fk(res, k):
    left, right = division(res)
    # Appel de la fonction F
    res_F = F(right, k)
    # Effectuer le xor entre le resultat de F et la partie gauche du resultat de IP
    return logical_xor(left,res_F )

# Switch : cette fonction commute les deux parties passes en parametre
def SW(res_fk1, right_ip):
    return right_ip + res_fk1

# Chiffrer un caractere (sur 8 bits) avec la cle k(chaine de caractere de 10 bits)
def chiffrement(char, key):
        
    # convert the binary string to an array of char
    charToBinary = text_to_bits(char)
    charToBinary_list = convert_to_list(charToBinary)

    # Generation des cles
    k1, k2 = generate_k(key)

    # Appliquer IP: la permutation initiale
    res_IP= IP(charToBinary_list)
    left_IP, right_IP = division(res_IP)
    
    # Appel de la fonction fk avec K1
    fk1 = fk(res_IP,k1)
    
    # Appel de la fonction SW
    sw_res = SW(fk1 ,right_IP )
    left_switch, right_switch = division(sw_res)
    
    # Appel de la fonction fk avec K2
    fk2 = fk(sw_res, k2)
    
    # Appel de la FP: permutation finale
    ciphertext_list = FP(fk2 + right_switch )
    
    # Conversion de la liste des caracteres en une chaine de caracteres 
    ciphertext = convert_list_to_char(ciphertext_list)

    return ciphertext


# Dechiffrer un ciphertext (resultat du chiffrement de plaintext) avec la cle k
def dechiffrement(ciphertext, key):
    if(len(ciphertext) != 8):
        print("Erreur : Le ciphertext doit etre une chaine de caracteres avec une longueur 8 bits composee de 0 et de 1 ")
        return -1
    # convert the binary string to an array of char
    charToBinary_list = convert_to_list(ciphertext)

    # Generation des cles
    k1, k2 = generate_k(key)

    # Appliquer IP: la permutation initiale
    res_IP= IP(charToBinary_list)
    left_IP, right_IP = division(res_IP)
    
    # Appel de la fonction fk avec K2
    fk2 = fk(res_IP,k2)
    
    # Appel de la fonction SW
    sw_res = SW(fk2 ,right_IP )
    left_switch, right_switch = division(sw_res)
    
    # Appel de la fonction fk avec K1
    fk1 = fk(sw_res, k1)
    
    # Appel de la FP: permutation finale
    res_final_list = FP(fk1 + right_switch )
    
    # Conversion de la liste des caracteres en une chaine de caracteres 
    res_final_char=convert_list_to_char(res_final_list)
    plaintext=text_from_bits(res_final_char)

    return plaintext

def main(char, key):
    if(len(key) != 2):
        print("Erreur: La cle doit etre une chaine de caracteres composee de deux caracteres")
        return False
    if(len(char) != 1):
        print("Erreur: Le plainText doit etre un caractere code sur 8 bits")
        return False
    
    # Convertir la cle en binaire
    key_to_binary=text_to_bits(key)
    # convert the binary string key to an array of char
    key_list=convert_to_list(key_to_binary)
    
    # Apres la conversion de la cle en binaire, on obtient 16 bits, on prend que les 10 premiers bits pour former une cle de 10 bits
    key_list_10 = []
    for i in range(0, 10):
        key_list_10.append(key_list[i])
        
    print('\nPlaintext :\t'+ char)
    print('Clef: '+ key)
    # Appel de la fonction chiffrement qui chiffre le caractere avec la clef passee en parametre 
    ciphertext = chiffrement(char, key_list_10)
    
    # Regarder si le chiffrement ne renvoie pas d erreur
    if(ciphertext != -1):
        print('Chiffrement du plainText "' + char + '" : '+ ciphertext)
        plaintext = dechiffrement(ciphertext, key_list_10)
        print('\nDecrypted:\t '+plaintext)
    
        if(char == plaintext):
            return True
        else:
            return False


plaintext = 'k'
key = 'C4'
# Recuperer le plaitext et la cle si ces derniers sont passes en argument en ligne de commande
if (len(sys.argv)>1):
        plaintext=str(sys.argv[1])
if (len(sys.argv)>2):
        key=str(sys.argv[2])
        
res = main(plaintext, key)
if(res):
    print("\nChiffrement et dechiffrement reussi XD !")
else:
    print("\nChiffrement et dechiffrement non reussi X( !")
    
