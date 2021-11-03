import random, math
from sympy import randprime
from keyUtil import saveKeyRSA
from mathHelper import *
from textUtil import block2pt, cipher2IntArr, pt2IntArr, pt2block

class RSA:
    def __init__(self, keySize=128):
        self.keySize = keySize
        self.e = None
        self.d = None
        self.n = None
    
    def modInv(self, a, m):
        g, x, _ = egcd(a,m)
        if g != 1:
            print("Modular Inverse is not exist")
        return x % m

    def generateKeyPair(self, p = 1, q = 1, e = 1):        
        if (p == 1 and q == 1):
            p = randprime(2**(self.keySize-1)+1, 2**self.keySize - 1)
            q = randprime(2**(self.keySize-1)+1, 2**self.keySize - 1)
        
        n = p*q
        totN = (p-1)*(q-1)
        
        if (e == 1):
            Terminate = False
            while not(Terminate):
                e = random.randrange(2**(self.keySize-1)+1, 2**self.keySize - 1)
                if (gcd(e, totN) == 1):
                    Terminate = True
            
        d = self.modInv(e, totN)

        # set value
        self.p = p
        self.q = q
        self.n = n
        self.d = d
        self.totN = totN
        self.e = e

    def encrypt(self, plaintext, e, n):
        # print(len(str(n))-1)
        # plain = pt2block(plaintext, len(str(n))-1)
        plain = pt2block(plaintext, (len(str(n)))-1)
        result = []
        resString = ''
        for block in plain:
            content = pow(block, e, n)
            resString += (str(content))
            result.append(content)
        return result, resString

    def decrypt(self, cipher, d, n):
        result = []
        for block in cipher:
            temp = pow(block, d, n)
            # result.append(str(temp).rjust(((len(str(n))-1)*3)//3, '0'))
            result.append(temp)
        plaintext = block2pt(result, (len(str(n))-1))
        return plaintext


def main():
    rsa = RSA()
    f = open("test.txt", "rb")
    pt = (f.read())
    f.close()
    rsa.generateKeyPair()
    saveKeyRSA(rsa.e, rsa.n, rsa.d, 'key1')
    ct, cts = rsa.encrypt(pt, rsa.e, rsa.n)
    for i in ct:
        print(len(str(i)))
    print(ct)
    # print(cts)
    # c = cipher2IntArr(cts, len(str(rsa.n)))
    c = cipher2IntArr(cts, (len(str(rsa.n))))
    print(c)
    for i in c:
        print (len(str(i)))
    # print(c==ct)
    print(rsa.decrypt(ct, rsa.d, rsa.n))


if __name__ == '__main__':
    main()
