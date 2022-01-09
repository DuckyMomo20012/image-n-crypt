import numpy as np
import random
import base64
import os
import cv2

BIT_NUMBER = 10

# tìm ước chung lớn nhất sử dụng thậ euclid mở rộn
def GCD(a,b):
    d,x,y = 0,0,0
    if b > a:
        a,b = b,a
    if b == 0:
        d,x,y = a,1,0
    x2,x1,y2,y1 = 1,0,0,1
    while b > 0:
        q = int(a/b)
        r = a - b * q
        a,b = b,r
        y = y2 -q*y1
        x = x2 - q* x1
        y2 = y1
        x2 = x1
        y1 = y
        x1 = x
    d,x,y = a,x2,y2
    return d,x,y

#Miller_Rabin
_mrpt_num_trials = 5
def is_probable_prime(n):
    assert n >= 2
    if n == 2:
         return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while True:
        thuong , du = divmod(d, 2)
        if du == 1:
            break
        s += 1
        d = thuong
    assert 2 ** s * d == n-1
    def try_composite(a):
        if pow(a, d, n) == 1: #a^d mod n
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True
    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
    return True


# kiểm tra nguyên tố
def check_prime(num):
    n = num
    if n < 0:
        n = -n
    count = 0
    for i in range(2,n):
        if num % i == 0:
            return False
    return True

# tính n = p*q
def calculate_n(p,q):
    return p * q   

# tính phi_n = (p-1) * (q -1)
def calculate_phi_n(p,q):
    return (p-1) * (q-1)

#sử dụng Miller để check prime
def creat_Prime(bit):
    p = random.getrandbits(bit)
    while is_probable_prime(p) != True or p == 1:
        p = random.getrandbits(bit)
        if p % 2 == 0:
            p = p | 1
    return p

# tạo hai số nguyên tố p và q
def creat_p_and_q(n):
    p = creat_Prime(n)
    q  = creat_Prime(n)
    while p == q:
        q  = creat_Prime(n)
    return p,q

# hàm genkey trả về n,e,d
def publicKey_privateKey(p,q):
    n = calculate_n(p,q)
    phi_n = calculate_phi_n(q,p)
    u,x,d = 0,0,0
    e = 0
    while u != 1:
        e =  random.randint(2, phi_n - 1)
        u,x,d= GCD(phi_n,e)
        if d < 0:
            d = phi_n + d
    return n,e,d

#pow mod
def powermod(x,e,n):
    y = e
    res = 1
    x = x % n
    if(x==0):
        return x
    while(y>0):
        if (y & 1)==1:
            res = int((res * x) % n)
        y = y >> 1
        x = int((int(x) * int(x)) % n)
    return res

# ghi file key
def create_write_key(path="", writeFile=False):
    p,q = creat_p_and_q(BIT_NUMBER)
    n,e,d = publicKey_privateKey(p,q)
    if writeFile:
        with open(path + "rsa_pub.txt", 'w') as publicKey:
            publicKey.write("{} {}".format(n,e))

        with open(path + "rsa.txt",'w') as private_key:
            private_key.write("{} {}".format(d, n))

    return e, d, n
    
def read_file(filename):
    with open(filename,'r') as f:
        data = f.read()
    return data


#ma hoa vì mã màu tối đa là 255 nên file save_quotient sẽ chưa thương của phần tử sau khi được mã hóa RSA.
def Encrypted(pathImage,path_pbKey,save_imageEncrypted = "eecode_imge.png", save_quotient = "quotient.txt"):
    img = cv2.imread(pathImage)
    public_key = read_file(path_pbKey)
    data = public_key.split(" ")
    n = int(data[0])
    e = int(data[1])
    str1 = ""
    f = open(save_quotient,'w')
    for i in range(3):
       for j in range(img.shape[0]):
            for l in range(img.shape[1]):
               tem = img[j,l,i]
               du1 = powermod(tem,e,n)
               du2 = powermod(du1,1,256)
               thuong = int(du1/256)
               img[j,l,i] = du2
               f.write(str(thuong)+ " ")
    f.close()
    cv2.imwrite(save_imageEncrypted,img)
    return img


def Decrypted(path_ImageDecode, path_private_key, save_imageDecrypted = "decode_imge.png", path_file_quotient ="quotient.txt"):
    img = cv2.imread(path_ImageDecode)
    private_key = read_file(path_private_key)
    quotient = read_file(path_file_quotient)
    list_quotient = quotient.split(" ")

    d_n = private_key.split(" ")
    d = int(d_n[0])
    n= int(d_n[1])
    index = 0
    for i in range(3):
       for j in range(img.shape[0]):
           for l in range(img.shape[1]):
               tem = img[j,l,i]
               c = tem +int(list_quotient[index]) * 256
               img[j,l,i] = powermod(c,d,n)
               index = index + 1
    cv2.imwrite(save_imageDecrypted,img)
    return img