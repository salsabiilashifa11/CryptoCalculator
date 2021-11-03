from sympy import randprime
from sympy.core.evalf import N
import random
from textUtil import *
from keyUtil import *
from mathHelper import *


class Paillier:
    def __init__(self, keySize=64):
        self.keySize = keySize
        self.n = None
        self.g = None
        self.lmd = None
        self.miu = None
    
    def generateKeyPair(self, p = 1, q = 1, g = 1):
        if (p == 1) and (q == 1):
            Terminate = False
            while not(Terminate):
                p = randprime(pow(2, self.keySize-1)+1, pow(2,self.keySize)-1)
                q = randprime(pow(2, self.keySize-1)+1, pow(2,self.keySize)-1)
                if (gcd(p*q, (p-1)*(q-1)) == 1):
                    Terminate  = True
        
        n = p*q
        self.n_sq = pow(n,2)
        lmd = lcm(p-1, q-1)

        if (g == 1):
            # Generate random integer
            g = random.randint(1, pow(n,2)-1)

        # declaring lambda for function L
        x = (pow(g, lmd, pow(n,2))-1)//n
        # Calculate miu
        miu = modInverse(x,n)

        self.n = n
        self.g = g
        self.lmd = lmd
        self.miu = miu


    def encrypt(self, plaintext, g):
        plain = pt2block(plaintext, len(str(self.n))-1)
        # print(plain)
        #  generate r
        
        result = []
        resStr = ''
        for block in plain:
            Terminate = False
            while not(Terminate):
                r = random.randint(0, self.n-1)
                if (r>=0 and r<self.n) and (gcd(r,self.n) == 1):
                    Terminate = True

            n_sq = pow(self.n, 2)
            x = pow(r, self.n, self.n_sq)
            tmp = pow(self.g, block, self.n_sq) * x % self.n_sq
            
            result.append(tmp)
            resStr += str(tmp)
        
        return result,resStr

    def decrypt(self, cipher, lmd, miu, n):
        result = []

        for block in cipher:
            x = pow(block, lmd, pow(self.n, 2)) - 1
            result.append(((x // self.n) * self.miu) % self.n)
        
        # print(result[0])
        plaintext = block2pt(result, len(str(pow(self.n, 2)))//2)
        return plaintext

def main():
    pail = Paillier()
    f = open("test.txt", "rb")
    pt = (f.read())
    f.close()
    pail.generateKeyPair()
    saveKeyPaillier(pail.n, pail.g, pail.miu, pail.lmd, 'keyPail')
    ct, cts = pail.encrypt(pt, pail.g)
    print(ct)
    c = cipher2IntArr(cts, len(str(pow(pail.n, 2))))
    print(c)
    print(pail.decrypt(c, pail.lmd, pail.miu, pail.n))


if __name__ == '__main__':
    main()
        
