import random
import os
import cv2

BIT_NUMBER = 10

from datetime import datetime


def getRandomFileName(fileName):
    return f"{fileName}_%s" % (datetime.now().strftime("%Y%m%d%H%M%S"))


# Find greatest common divisor (GCD) using Extended Euclid
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


# Miller_Rabin
_mrpt_num_trials = 5


def isProbablePrime(n):
    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert 2**s * d == n - 1

    def tryComposite(a):
        if pow(a, d, n) == 1:  # a^d mod n
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n - 1:
                return False
        return True

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if tryComposite(a):
            return False
    return True


# Check prime
def checkPrime(num):
    n = num
    if n < 0:
        n = -n
    for i in range(2, n):
        if num % i == 0:
            return False
    return True


def calculate_n(p, q):
    return p * q


def calculate_phi_n(p, q):
    return (p - 1) * (q - 1)


# Use Miller Rabin to check prime
def generatePrime(bit):
    p = random.getrandbits(bit)
    while isProbablePrime(p) != True or p == 1:
        p = random.getrandbits(bit)
        if p % 2 == 0:
            p = p | 1
    return p


# Generate prime p and q
def generate_p_and_q(n):
    p = generatePrime(n)
    q = generatePrime(n)
    while p == q:
        q = generatePrime(n)
    return p, q


# Generate public key and private key
def generateKeys(p, q):
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


def powermod(x, e, n):
    y = e
    res = 1
    x = x % int(n)
    if x == 0:
        return x
    while y > 0:
        if (y & 1) == 1:
            res = int((res * x) % n)
        y = y >> 1
        x = int((int(x) * int(x)) % n)
    return res


# Write keys to files
def generateAndWriteKeyToFile(dstPath="", writeFile=False):
    p, q = generate_p_and_q(BIT_NUMBER)
    n, e, d = generateKeys(p, q)
    if writeFile:
        fileName = "rsa.txt"
        if os.path.exists(fileName):
            splitFileName, ext = os.path.splitext(fileName)
            fileName = getRandomFileName(splitFileName) + ext
        with open(dstPath + "rsa_pub.txt", "w") as publicKey:
            publicKey.write("{} {}".format(n, e))

        with open(dstPath + fileName, "w") as private_key:
            private_key.write("{} {}".format(d, n))

    return e, d, n


def readFile(filename):
    with open(filename, "r") as f:
        data = f.read()
    return data


# Because color code has maximum is 255, so file quotientSaveDst will store
# quotient of each pixels after encrypted.
def Encrypted(
    imgPath,
    e=None,
    n=None,
    publicKeyPath=None,
    imgEncryptedSaveDst="encode_img.png",
    quotientSaveDst="quotient.txt",
):
    if not publicKeyPath and not e and not n:
        raise Exception("Public key is missing")
    # e, n directly passed into function has more priority than text file
    if publicKeyPath and not e and not n:
        publicKey = readFile(publicKeyPath)
        n, e = map(int, publicKey.split(" "))

    if not e or not n and not publicKeyPath:
        raise Exception("Public key is missing.")

    if not os.path.exists(imgPath):
        raise Exception("Image path is not exist")

    img = cv2.imread(imgPath)

    f = open(quotientSaveDst, "w")
    for i in range(3):
        for j in range(img.shape[0]):
            for l in range(img.shape[1]):
                pixel = img[j, l, i]
                remainder1 = powermod(pixel, e, n)
                remainder2 = powermod(remainder1, 1, 256)
                quotient = int(remainder1 / 256)
                img[j, l, i] = remainder2
                f.write(str(quotient) + " ")
    f.close()
    cv2.imwrite(imgEncryptedSaveDst, img)
    return img


def Decrypted(
    imgEncryptedPath,
    d=None,
    n=None,
    privateKeyPath=None,
    imgDecryptedSaveDst="decode_img.png",
    quotientPath="quotient.txt",
):
    if not privateKeyPath and not d and not n:
        raise Exception("Private key is missing")
    # d, n directly passed into function has more priority than text file
    if privateKeyPath and not d and not n:
        private_key = readFile(privateKeyPath)
        d, n = map(int, private_key.split(" "))

    if not os.path.exists(imgEncryptedPath):
        raise Exception("Image path is not exist")

    if not os.path.exists(quotientPath):
        raise Exception("Quotient path is not exist")

    img = cv2.imread(imgEncryptedPath)
    quotient = readFile(quotientPath)
    list_quotient = quotient.split(" ")

    index = 0
    for i in range(3):
        for j in range(img.shape[0]):
            for l in range(img.shape[1]):
                pixel = img[j, l, i]
                c = pixel + int(list_quotient[index]) * 256
                img[j, l, i] = powermod(c, d, n)
                index = index + 1
    cv2.imwrite(imgDecryptedSaveDst, img)
    return img
