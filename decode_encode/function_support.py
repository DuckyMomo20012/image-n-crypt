import numpy as np
import random
import base64
import os
import cv2

BIT_NUMBER = 10
# tìm ước chung lớn nhất sử dụng thậ euclid mở rộn
def GCD(a, b):
    d, x, y = 0, 0, 0
    if b > a:
        a, b = b, a
    if b == 0:
        d, x, y = a, 1, 0
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q = int(a / b)
        r = a - b * q
        a, b = b, r
        y = y2 - q * y1
        x = x2 - q * x1
        y2 = y1
        x2 = x1
        y1 = y
        x1 = x
    d, x, y = a, x2, y2
    return d, x, y


# kiểm tra nguyên tố
def check_prime(num):
    n = num
    if n < 0:
        n = -n
    count = 0
    for i in range(2, n):
        if num % i == 0:
            return False
    return True


# tính n = p*q
<<<<<<< Updated upstream
def calculate_n(p,q):
    return p * q   
=======
def calculate_n(p, q):
    return p * q
>>>>>>> Stashed changes


# tính phi_n = (p-1) * (q -1)
def calculate_phi_n(p, q):
    return (p - 1) * (q - 1)


<<<<<<< Updated upstream
# tạo số nguyên nguyên tố khoảng 24 bits trở xuống, lớn quá hàm check_Prime 
def creat_Prime(bit):
=======
# tạo số nguyên nguyên tố khoảng 24 bits trở xuống, lớn quá hàm check_Prime
def create_Prime(bit):
>>>>>>> Stashed changes
    p = random.getrandbits(bit)
    while check_prime(p) != True or p == 1:
        p = random.getrandbits(bit)
        if p % 2 == 0:
            p = p | 1
    return p


# tạo hai số nguyên tố p và q
def create_p_and_q(n):
    p = create_Prime(n)
    q = create_Prime(n)
    while p == q:
        q = create_Prime(n)
    return p, q


# hàm genkey trả về n,e,d
def publicKey_privateKey(p, q):
    n = calculate_n(p, q)
    phi_n = calculate_phi_n(q, p)
    u, x, d = 0, 0, 0
    e = 0
    while u != 1:
        e = random.randint(2, phi_n - 1)
        u, x, d = GCD(phi_n, e)
        if d < 0:
            d = phi_n + d
    return n, e, d


# pow mod
def powermod(x, e, n):
    y = e
    res = 1
    x = x % n
    if x == 0:
        return x
    while y > 0:
        if (y & 1) == 1:
            res = (res * x) % n
        y = y >> 1
        x = (x * x) % n
    return res


# ghi file key
<<<<<<< Updated upstream
def create_write_key():
    p,q = creat_p_and_q(BIT_NUMBER)
    n,e,d = publicKey_privateKey(p,q)
    path =""
    f = open(path + "rsa_pub.txt",'w')
    f.write("{} {}".format(n,e))
    f.close()
    f1 = open(path+ "rsa.txt",'w')
    f1.write("{} {}".format(d, n))
    f1.close()
    
=======
def create_write_key(path="", writeFile=False):
    p, q = create_p_and_q(BIT_NUMBER)
    n, e, d = publicKey_privateKey(p, q)
    if writeFile:
        with open(path + "rsa_pub.txt", "w") as publicKey:
            publicKey.write("{} {}".format(n, e))

        with open(path + "rsa.txt", "w") as privateKey:
            privateKey.write("{} {}".format(d, n))

    return e, d, n




>>>>>>> Stashed changes
def read_file(filename):
    with open(filename, "r") as f:
        data = f.read()
    return data


# ma hoa
def Encrypted(path_pbKey, inputFilePath, outputFilePath = "encrypted.txt"):
    public_key = read_file(path_pbKey)
    data = public_key.split(" ")
    n = int(data[0])
    e = int(data[1])
<<<<<<< Updated upstream
    list_encryp ="DONE"
    base64_encoded_data = base64.b64encode(image)
    base64_message = base64_encoded_data.decode('utf-8')
    f = open("encrypted.txt",'w')
=======
    list_encrypt = "DONE"
    base64_encoded_data = base64.b64encode(inputFilePath)
    base64_message = base64_encoded_data.decode("utf-8")
    f = open(outputFilePath, "w")
>>>>>>> Stashed changes
    for i in base64_message:
        tem = ord(i)
        c = powermod(tem, e, n)
        tr1 = str(c)
        f.write(tr1 + " ")
    f.close()
    return list_encrypt


def Decrypted(path_private_key, pathEncode, outputFilePath = "decoded_image.png"):
    data = read_file(pathEncode)
    private_key = read_file(path_private_key)
    d_n = private_key.split(" ")
    d = int(d_n[0])
<<<<<<< Updated upstream
    n= int(d_n[1])
    
=======
    n = int(d_n[1])

>>>>>>> Stashed changes
    list_base64 = data.split(" ")
    base64_img = ""
    for i in list_base64:
        if len(i) != 0:
            c = powermod(int(i), d, n)
            h = chr(c)
            base64_img = base64_img + h

    base64_img_bytes = base64_img.encode("utf-8")
    file_to_save = open(outputFilePath, "wb")
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    file_to_save.write(decoded_image_data)
    file_to_save.close()
    return decoded_image_data
