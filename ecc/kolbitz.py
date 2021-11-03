from math import floor

def encode(a, b, p, char, k):
    m = ord(char)
    x = m*k + 1
    found = False
    result = 0
    
    while (not found):
        target_remainder = (x**3 + a*x + b) % p
        for i in range(p):
            if ((i**2) % p == target_remainder):
                found = True
                result = i
                break
        if (not found):
            x += 1

    return ((x, result))

def decode(pair, k):
    return floor((pair[0] - 1)/k)

# encoded = encode(-1, 188, 751, '1', 20)
# decoded = decode(encoded, 20)

# print(encoded)
# print(chr(decoded))
