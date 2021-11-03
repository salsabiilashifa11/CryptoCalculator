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

def generate_key(nbits):
    p = randprime(pow(2, nbits-1)+1, pow(2, nbits)-1)
    g = random.randint(1, pow(10, 6))
    x = random.randint(1, pow(10, 6))
    y = (g**x) % p
    pub = (y, g, p)
    pri = (x, p)

    return (pub, pri)

def encrypt(plaintext, y, g, p):
    result = []
    for char in plaintext:
        k = random.randint(1, pow(10, 4))
        a = (g**k) % p 
        b = (y**k * ord(char)) % p 
        result.append((a, b))
    return result 

def decrypt(ciphertext, x, p):
    result = ""
    for tup in ciphertext:
        result += chr((tup[1] * (modinv(tup[0]**x, p))) % p)
    return result    

key = generate_key(32)
pub = key[0]
pri = key[1]

enciphered = encrypt('shifa', pub[0], pub[1], pub[2])
deciphered = decrypt(enciphered, pri[0], pri[1])

print(enciphered)
print(deciphered)

