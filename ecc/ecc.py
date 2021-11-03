from curve import generate_points, scalar_multiplication, point_addition
from kolbitz import encode, decode
import random
from sympy import randprime

# #Get all required variables
# a = int(input("Masukkan a: "))
# b = int(input("Masukkan b: "))
# p = int(input("Masukkan p: "))

# points = generate_points(a, b, p)

# baseP = points[random.randint(0, len(points)-1)] #--> Buat nanti kalo udah bener
# # baseP = points[5]

# na = int(input("Masukkan private key 1: "))
# pa = scalar_multiplication(a, b, p, na, baseP)

# nb = int(input("Masukkan private key 2: "))
# pb = scalar_multiplication(a, b, p, nb, baseP)

def curve_generator(nbits, filename):
    p = randprime(pow(2, nbits-1)+1, pow(2, nbits)-1)
    a = random.randint(2, pow(10, 2))
    b = random.randint(2, pow(10, 2))

    points = generate_points(a, b, p)
    baseP = points[random.randint(0, len(points)-1)]

    save_curve(a, b, p, baseP, filename)
    return (a, b, p, baseP)


def key_generator(a, b, p, baseP, nbits, filename):
    pri = randprime(2, pow(2, nbits-1)+1)
    pub = scalar_multiplication(a, b, p, pri, baseP)

    save_key(pub, filename + ".pub")
    save_key(pri, filename + ".pri") 
    return (pub, pri)

def save_curve(a, b, p, baseP, fname):
    fname = "../save/ecc/curve/" + fname
    with open(fname, "w") as f:
        f.write("%s\n" % a)
        f.write("%s\n" % b)
        f.write("%s\n" % p)
        for element in baseP:
            f.write("%s " % element)
    f.close()

def save_key(key, fname):
    fname = "../save/ecc/key/" + fname
    with open(fname, "w") as f:
        if (fname[-3:] == "pri"):
            f.write("%s" % key)
        elif (fname[-3:] == "pub"):
            for element in key:
                f.write("%s " % element)
    f.close()

def save_enc(msg, fname):
    fname = "../save/ecc/enc/" + fname
    with open(fname, "w") as f:
        for cipher in msg:
            for pair in cipher:
                for element in pair:
                    f.write("%s " % element)
            f.write("\n")
    f.close()

def read_enc(fname):
    msg = []
    fname = "../save/ecc/enc/" + fname
    f = open(fname, "r")
    for line in f:
        content = line.rstrip().split()
        tup1 = (int(content[0]), int(content[1]))
        tup2 = (int(content[2]), int(content[3]))
        msg.append((tup1, tup2))
    return msg

def read_curve(fname):
    fname = "../save/ecc/curve/" + fname
    f = open(fname, "r")
    a = int(f.readline().rstrip())
    b = int(f.readline().rstrip())
    p = int(f.readline().rstrip())
    point_content = f.readline().rstrip().split()
    baseP = (int(point_content[0]), int(point_content[1]))
    return (a, b, p, baseP)

def read_key(fname):
    fname = "../save/ecc/key/" + fname
    f = open(fname, "r")
    if (fname[-3:] == "pri"):
        key = int(f.readline().rstrip())
    else: #pub
        point_content = f.readline().rstrip().split()
        key = (int(point_content[0]), int(point_content[1]))
    return key
    


# INI MULAI ENKRIPSINYA
def encrypt(a, b, p, baseP, pb, enckey, plaintext):
    k = random.randint(1, p-1)
    result = []
    for char in plaintext:
        pm = encode(a, b, p, char, enckey)
        pc = [0,0]

        pc[0] = scalar_multiplication(a, b, p, k, baseP)
        pc[1] = point_addition(p, a, pm, scalar_multiplication(a, b, p, k, pb))

        result.append((pc[0], pc[1]))
    return result

def decrypt(a, b, p, baseP, nb, enckey, ciphertext):
    result = ""
    for tup in ciphertext:
        key = scalar_multiplication(a, b, p, nb, tup[0])
        minus_key = (key[0], (key[1]*-1)%p)
        pm = point_addition(p, a, tup[1], minus_key)
        result += chr(decode(pm, enckey))
    return result


#SIMUL MAIN
# curve = curve_generator(16, "curve.txt")
# keyA = key_generator(curve[0], curve[1], curve[2], curve[3], 8, "keyA")
# keyB = key_generator(curve[0], curve[1], curve[2], curve[3], 8, "keyB")
# print(keyA[0])
# print(keyA[1])

# enciphered = encrypt(curve[0], curve[1], curve[2], curve[3], keyA[0], 10, "Kita cobain teks yang agak panjang gan")
# save_enc(enciphered, 'save_test.txt')
# deciphered = decrypt(curve[0], curve[1], curve[2], curve[3], keyA[1], 10, enciphered)

# print(enciphered)
# print(deciphered)

        
#READ FILE
curve = read_curve("curve.txt")
keyA = (read_key("keyA.pub"), read_key("keyA.pri"))
enciphered = read_enc("save_test.txt")
deciphered = decrypt(curve[0], curve[1], curve[2], curve[3], keyA[1], 10, enciphered)
print(deciphered)
    



