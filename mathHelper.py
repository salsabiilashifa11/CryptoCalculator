import math


def gcd(a,b):
    # euclidean gcd
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def lcm(a,b):
    return (a*b // gcd(a,b))

def egcd(a, b):
    #Extended euclidean gcd
    if (a == 0):
        return (b, 0, 1)
    else:
        g,y,x = egcd(b%a, a)
        return (g, x-(b//a)*y, y)

def modInv(e, totN):
    d = None
    i = 1
    terminate = False

    while not terminate:
        temp = totN*i +1
        d = float(temp/e)
        d_int = int(d)
        i += 1
        if (d_int == d):
            terminate = True
    return d_int

def modular_power(basis, exp, modulus):
    return pow(basis, exp, modulus)

def modInverse(a, m):
    g, x, y = egcd(a, m)
    if (g != 1):
        print("modular inverse does not exist")
    else:
        return x % m

def main():
    print(modular_power(5,124,3))

if __name__ == '__main__':
    main()
