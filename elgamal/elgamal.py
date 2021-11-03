from sympy import randprime
import random

# Extended Euclidean algorithm
def extended_gcd(aa, bb):
   lastremainder, remainder = abs(aa), abs(bb)
   x, lastx, y, lasty = 0, 1, 1, 0
   while remainder:
       lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
       x, lastx = lastx - quotient*x, x
       y, lasty = lasty - quotient*y, y
   return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# calculate `modular inverse`
def modinv(a, m):
   g, x, y = extended_gcd(a, m)
   if g != 1:
       raise ValueError
   return x % m

def elgamal_generate_key(nbits, path):
    p = randprime(pow(2, nbits-1)+1, pow(2, nbits)-1)
    g = random.randint(1, pow(10, 6))
    x = random.randint(1, pow(10, 6))
    y = (g**x) % p
    pub = (y, g, p)
    pri = (x, p)

    elgamal_save_key(y, g, p, x, path)
    return (pub, pri)

def elgamal_save_key(y, g, p, x, path):
    pubkey = "save/elGamal/key/" + path + ".pub"
    prikey = "save/elGamal/key/" + path + ".pri"

    with open(pubkey, "w") as f:
        f.write("%s\n" % y)
        f.write("%s\n" % g)
        f.write("%s" % p)
    f.close()

    with open(prikey, "w") as r:
        r.write("%s\n" % x)
        r.write("%s" % p)
    r.close()

def elgamal_save_enc(msg, fname):
    with open(fname, "w") as f:
        for cipher in msg:
            for element in cipher:
                f.write("%s " % element)
            f.write("\n")
    f.close()

def elgamal_read_enc(fname):
    msg = []
    f = open(fname, "r")
    for line in f:
        content = line.rstrip().split()
        tup = (int(content[0]), int(content[1]))
        msg.append(tup)
    return msg

def elgamal_read_key(fname):
    f = open(fname, "r")
    if (fname[-3:] == "pri"):
        point_content = f.readline().rstrip().split()
        key = (int(point_content[0]), int(point_content[1]))
    else: #pub
        point_content = f.readline().rstrip().split()
        key = (int(point_content[0]), int(point_content[1]), int(point_content[2]))
    return key

def elgamal_encrypt(plaintext, y, g, p):
    result = []
    for char in plaintext:
        k = random.randint(1, pow(10, 4))
        a = (g**k) % p 
        b = (y**k * ord(char)) % p 
        result.append((a, b))
    return result 

def elgamal_decrypt(ciphertext, x, p):
    result = ""
    for tup in ciphertext:
        result += chr((tup[1] * (modinv(tup[0]**x, p))) % p)
    return result    



