from operator import xor
import binascii

s0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

s1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]
#utiliser libssl pour le prochain tp
def convert_to_list(str):

  string_length = len(str)
  tab = []
  for i in range(0, string_length):
    tab.append(str[i])
  return tab;

def convert_list_to_char(lst):
    ch=''
    for i in range(0,len(lst)):
        ch=ch+lst[i]
    return ch

def permute_10(key):
    tab = []
    tab.append(key[2])
    tab.append(key[4])
    tab.append(key[1])
    tab.append(key[6])
    tab.append(key[3])
    tab.append(key[9])
    tab.append(key[0])
    tab.append(key[8])
    tab.append(key[7])
    tab.append(key[5])
    return tab

def permute_8(key):
    tab = []
    tab.append(key[5])
    tab.append(key[2])
    tab.append(key[6])
    tab.append(key[3])
    tab.append(key[7])
    tab.append(key[4])
    tab.append(key[9])
    tab.append(key[8])

    return tab


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

def division(param):
    left_half = []
    right_half = []
    for i in range(0, len(param)):
        if(i < len(param)/2):
            left_half.append(param[i])
        else:
            right_half.append(param[i])

    return left_half, right_half

# concatenation des deux demis clefs apres la rotation circulaire a gauche (LS_1 + L_S1)
def concat_ls_keys(left, right):
    tab = []
    tab = left + right
    return tab


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

# initial permutation
def IP(plaintext):
    tab = []
    tab.append(plaintext[1])
    tab.append(plaintext[5])
    tab.append(plaintext[2])
    tab.append(plaintext[0])
    tab.append(plaintext[3])
    tab.append(plaintext[7])
    tab.append(plaintext[4])
    tab.append(plaintext[6])
    return tab

# final permutation (inverse de IP)
def FP(plaintext):
    tab = []
    tab.append(plaintext[3])
    tab.append(plaintext[0])
    tab.append(plaintext[2])
    tab.append(plaintext[4])
    tab.append(plaintext[6])
    tab.append(plaintext[1])
    tab.append(plaintext[7])
    tab.append(plaintext[5])
    return tab

# EP = Expansion/permutation
# utiliser 4 bits de droite du resultat de IP
def EP(half_right_result_IP):
    tab = []
    tab.append(half_right_result_IP[3])
    tab.append(half_right_result_IP[0])
    tab.append(half_right_result_IP[1])
    tab.append(half_right_result_IP[2])
    tab.append(half_right_result_IP[1])
    tab.append(half_right_result_IP[2])
    tab.append(half_right_result_IP[3])
    tab.append(half_right_result_IP[0])
    return tab

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

def conversion_to_decimal(x):
    res = 0
    for i in range(0, len(x)):
        if(x[i] == '1'):
            res += pow(2,len(x)-i-1)

    return res

def permute_4(res_s0_s1):
    tab = []
    tab.append(res_s0_s1[1])
    tab.append(res_s0_s1[3])
    tab.append(res_s0_s1[2])
    tab.append(res_s0_s1[0])
    return tab


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


#left, right = division() a appeler dans f et appeler cette methose avec le resultat
def F(right_half_IP, k1):
    res_EP = EP(right_half_IP)
    #print 'ep', res_EP
    res_xor_EP_K1 = xor_EP_K1(res_EP, k1)
    #print 'res_xor_EP_K1',res_xor_EP_K1
    line_s0 = conversion_to_decimal([res_xor_EP_K1[0], res_xor_EP_K1[3]])
    #print 'line_s0',line_s0
    column_s0 = conversion_to_decimal([res_xor_EP_K1[1], res_xor_EP_K1[2]])
    #print 'column_s0',column_s0
    res_S0 = s0[line_s0][column_s0]
    #print 'res_S0',res_S0
    binary_res_s0 = conversion_to_binary(res_S0)
    #print 'binary_res_s0',binary_res_s0
    line_s1 = conversion_to_decimal([res_xor_EP_K1[4], res_xor_EP_K1[7]])
    column_s1 = conversion_to_decimal([res_xor_EP_K1[5], res_xor_EP_K1[6]])
    res_S1 = s1[line_s1][column_s1]
    #print 'res_S1',res_S1
    binary_res_s1 = conversion_to_binary(res_S1)
    #print 'binary_res_s1',binary_res_s1
    p4 = permute_4(binary_res_s0 + binary_res_s1)
    #print 'p4',p4
    return p4
    

def fk(res, k):
    left, right = division(res)
    res_F = F(right, k)
    return logical_xor(left,res_F )

def SW(res_fk1, right_ip):
    return right_ip + res_fk1


#res = conversion_to_decimal(['1','1','1'])
#print(res,"jlikqsqjsf")
#
#k1, k2 = generate_k(['1','0','1','0','0','0','0','0','1','0'])
#print "k1",k1
#print "k2",k2
#
#xorr = logical_xor(['1','1','0','1'], ['1','0', '0','1'])
#print("xorr",xorr)
#
#l= conversion_to_binary(5)
#print "conversion binary",l
##a regarder
#res_IP= IP(['1','0','1','0','1','0','0','0'])
#print 'res_ip',res_IP
#left, right = division(res_IP)
#
#
#fk1 = fk(res_IP,k1)
#print('fk1',fk1)
#sw_test = SW(fk1 ,right )
#print 'sw_test',sw_test
#
#
#fk2 = fk(sw_test, k2)
#print 'fk2', fk2
#
#left_switch, right_switch = division(sw_test)
#res_final = FP(fk2 + right_switch )
#print 'res_final',res_final
#
#
#test = conversion_to_decimal([1,1])
#print 'test',test
#
#print 'log',logical_xor(['1', '0', '0', '0'],['0', '0', '1', '1'])
#
#print str(5)

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

# La cle doit etre une chaine de caracteres
def chiffrement(char, key):
    if(len(char) != 1):
        print("Le plainText doit etre un caractere code sur 8 bits")
        return -1
    if(len(key) != 10):
        print("La cle doit etre une chine de caracteres avec une longueur 10 ")
        return -1
    # convert the binary string to an array of char
    charToBinary = text_to_bits(char)
    charToBinary_list = convert_to_list(charToBinary)

    # convert the binary string key to an array of char
    key_list = convert_to_list(key)

    # Generation des cles
    k1, k2 = generate_k(key_list)

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


# La cle doit etre une chaine de caracteres composees de chiffres 0 et 1 
def dechiffrement(ciphertext, key):
    if(len(ciphertext) != 8):
        print("Le ciphertext doit etre une chaine de caracteres avec une longueur 8 composee de 0 et de 1 ")
        return -1
    if(len(key) != 10):
        print("La cle doit etre une chaine de caracteres avec une longueur 10 ")
        return -1
    # convert the binary string to an array of char
    charToBinary_list = convert_to_list(ciphertext)

    # convert the binary string key to an array of char
    key_list = convert_to_list(key)

    # Generation des cles
    k1, k2 = generate_k(key_list)

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
    print('PlainText avant le chiffrement: ',char)
    
    ciphertext = chiffrement(char, key)
    print('Chiffrement',ciphertext)
    
    plaintext = dechiffrement(ciphertext, key)
    print('PlainText apres le dechiffrement: ',plaintext)
    
    if(char == plaintext):
        return True
    else:
        return False
    #return False
  

res = main('k', '1234567890')
if(res):
    print("Chiffrement et dechiffrement reussi XD !")
else:
    print("Chiffrement et dechiffrement non reussi X( !")
    
