import random

def shift_encrypt(key,msg):
    x = 0
    ctx = ''
    while x < len(msg):
        ctx += chr((ord(msg[x]) - 97 + key) % 26 + 97)
        # 평문을 아스키코드로 변환 후 계산을 위해 a의 아스키 값을 0으로 만듦
        # -97을 하고 key를 더한 후 mod 26 후 아스키 값 복원 +27 
        x+=1
    return ctx

def shift_decrypt(key, ctx):
    x = 0
    msg = ''
    while x < len(ctx):
        msg += chr((ord(ctx[x]) - 97 - key) % 26 + 97)
        x+=1
    return msg


def vigenere_genkey(n):
    x = 0
    key = []
    while x < n:
        key.append(random.randint(0,25))
        x+=1
    return key

def vigenere_encrypt(key,msg):
    x = 0
    ctx = ''
    while x<len(msg):
        ctx += chr((ord(msg[x]) - 97 + key[x%len(key)]) % 26 + 97)
        x+=1
    return ctx

def vigenere_decrypt(key, ctx):
    x = 0
    msg = ''
    while x < len(ctx):
        msg += chr((ord(ctx[x]) - 97 - key[x%len(key)]) % 26 + 97)
        x+=1
    return msg

def lfsr_genkeysteam(n):
    x = 0
    y = 0
    cont = []
    key = []
    while x < n:
        cont.append(random.randint(0,25)) 
        key.append(random.randint(0,25))    # 랜덤한 key 생성
        x+=1
    keyteam = (cont, key)
    return keyteam

def lfsr_encrypt(key,msg):  
    x = 0
    y = 0
    i = 0
    sum = 0
    ctx = ''
    while x < len(msg):
        while i < len(key[0]) :
            sum += key[0][i]*key[1][x+i]  # x_n+m = c_0*x_n + c_1*x_n+1 + ... + c_m*x_n+m-1
            i+=1
        i = 0
        key[1].append(sum % 26)
        x+=1
    while y < len(msg):
        ctx += chr(((ord(msg[y]) - 97) + key[1][len(key[0])+y]) % 26 + 97) # 평문과 key값으로 생성한 랜덤한 수를 연
        y+=1
    return ctx

    
def lfsr_decrypt(key,ctx):
    x = 0
    y = 0
    i = 0
    sum = 0
    msg = ''
    while x < len(ctx):
        while i < len(key[0]) :
            sum += key[0][i]*key[1][x+i]
            i+=1
        i = 0
        key[1].append(sum % 26)
        x+=1
    while y < len(ctx):
        msg += chr(((ord(ctx[y]) - 97) + 26 - key[1][len(key[0])+y]) % 26 + 97)
        y+=1
    return msg


