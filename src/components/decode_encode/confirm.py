from numpy import char
from function_support import *

def confirm(n,e,d):
    s = 'i have publicKey'
    temp = ""
    encode = []
    #encrypt
    for i in s:
        c = powermod(ord(i),e,n)
        encode.append(c)
    #decrypt
    for i in encode:
        m = powermod(i,d,n)
        print(m)
        temp = temp + chr(m)
    print(temp)
    if s == temp:
        return True 
    else:
        return False

