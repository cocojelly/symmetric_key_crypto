import random

##################################SimpleDES##################################

def sdes_expand(rblock): #E(R)
     Erblock = rblock[0:2]
     Erblock.append(rblock[3])
     Erblock.append(rblock[2])
     Erblock.append(rblock[3])
     Erblock.append(rblock[2])
     Erblock += rblock[4:6]
     return Erblock 

def sdes_keyschedule(key,rindex): #key -> roundkey(k1, k2, ... )
    if rindex == 1:
        roundkey = key[0:8]
    elif rindex == 2:
        roundkey = key[1:9]
    elif rindex == 3:
        roundkey = key[2:9] + [key[0]]
    return roundkey
# k1 : key[0~7]
# k2 : key[1~8]
# k3 : key[2~8, 0]

def sdes_sbox(s, index): #Sbox
    s_output =  []
    #sbox1 = [101 010 001 110 011 100 111 000 / 001 100 110 010 000 111 101 011]
    #sbox2 = [100 000 110 101 111 001 011 010 / 101 011 000 111 110 010 001 100]
    sbox1 = [[1,0,1,0,1,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,0], [0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,1,1,1,1,0,1,0,1,1]]
    sbox2 = [[1,0,0,0,0,0,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,1,0], [1,0,1,0,1,1,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,1,0,0]]
    index1 = s[0]
    index2 = s[1]*4 + s[2]*2 + s[3]*1
    if index == 1:
        s_output+=sbox1[index1][index2*3:index2*3+3]
    elif index == 2:
        s_output+=sbox2[index1][index2*3:index2*3+3]
    return s_output 
        
def sdes_compute_function(rblock, roundkey): #f function
    n = 0
    s_input = []
    Erblock = sdes_expand(rblock)
    while n < 8:
        s_input.append(Erblock[n] ^ roundkey[n])
        n+=1
    return sdes_sbox(s_input[0:4], 1) + sdes_sbox(s_input[4:8], 2)


def sdes_encrypt(key, pblock):      #pblock은 길이 12의 리스트로만 들어온다고 가정
    # R_i+1 = L_i ^ f(R_i, k_i-1)
    
    l0 = pblock[0:6]
    r0 = pblock[6:12]

    n = 0               
    l1 = r0
    f1 = sdes_compute_function(r0, sdes_keyschedule(key,1))
    r1 = []
    while n < 6:
        r1.append(l0[n] ^ f1[n])
        n+=1

    n = 0
    l2 = r1
    f2 = sdes_compute_function(r1, sdes_keyschedule(key,2))
    r2 = []
    while n < 6:
        r2.append(l1[n] ^ f2[n])
        n+=1

    n = 0
    l3 = r2
    f3 = sdes_compute_function(r2, sdes_keyschedule(key,3))
    r3 = []
    while n < 6:
        r3.append(l2[n] ^ f3[n])
        n+=1
        
    cblock = l3 + r3
    return cblock 


def sdes_decrypt(key, cblock):
    l3 = cblock[0:6]
    r3 = cblock[6:12]

    n = 0
    r2 = l3
    f3 = sdes_compute_function(r2, sdes_keyschedule(key,3))
    l2 = []
    while n < 6:
        l2.append(r3[n] ^ f3[n])
        n+=1            

    n = 0
    r1 = l2
    f2 = sdes_compute_function(r1, sdes_keyschedule(key,2))
    l1 = []
    while n < 6:
        l1.append(r2[n] ^ f2[n])
        n+=1

    n = 0
    r0 = l1
    f1 = sdes_compute_function(r0, sdes_keyschedule(key,1))
    l0 = []
    while n < 6:
        l0.append(r1[n] ^ f1[n])
        n+=1
    
    pblock = l0 + r0
    return pblock 

##################################CBC##################################
	
	
def cbc_genkey():  #9비트(길이가 9인 리스트) key를 생성
    n = 0
    key = []
    while n < 9:
        key.append(random.randint(0,1))
        n+=1
    return key
	
def cbc_encrypt(keybits, ivbits, plainbits):	#encryption
	n = 0
	cipherbits = []
	for i in range(len(plainbits)):
		if i < 12:
			plainbits[i] = plainbits[i] ^ ivbits[i]
		else:
			plainbits[i] = plainbits[i] ^ cipherbits[i-12]
		if i != 0 and (i+1) % 12 == 0:
			cipherbits[i-11:i+1] = sdes_encrypt(keybits, plainbits[i-11:i+1])
		
	return cipherbits
	
def cbc_decrypt(keybits, ivbits, cipherbits):	#decryption
	n = 0
	plainbits = []
	for i in range(len(cipherbits)-1, -1, -1):
		if (i+1) % 12 == 0:
			cipherbits[i-11:i+1] = sdes_decrypt(keybits, cipherbits[i-11:i+1])
		if i > 11:
			plainbits.insert(0, cipherbits[i] ^ cipherbits[i-12])
		else:
			plainbits.insert(0, cipherbits[i] ^ ivbits[i])
			
	return plainbits
