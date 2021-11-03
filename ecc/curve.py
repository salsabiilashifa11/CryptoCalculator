import itertools

def generate_points(a, b, p):
    xlable = dict()
    ylable = dict()

    def lablex(x):
        xlable.setdefault((x**3+a*x+b)%p, []).append(x)

    def labley(y):
        ylable.setdefault((y**2)%p, []).append(y)

    for num in range(0,p):
        lablex(num)
        labley(num)

    intersect = []
    for item in xlable.keys():
        if item in ylable:
            tmp = list(itertools.product(xlable[item], ylable[item]))
            intersect = intersect + tmp;
    intersect = sorted(intersect)
    return intersect

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

def scalar_multiplication(a, b, p, factor, point):
    x0 = point[0]
    y0 = point[1]

    for i in range(2, factor+1):
        s = 0
        if (x0 == point[0]):
            s = ((3 * (point[0] ** 2) + a) * modinv(2 * point[1], p))%p
        else:
            s = ((y0 - point[1]) * modinv(x0 - point[0], p))%p
    
        x3 = (s ** 2 - point[0] - x0) % p
        y3 = (s*(point[0] - x3) - point[1]) % p
        (x0, y0) = (x3, y3)

    return (x3, y3)


def point_addition(p, A, P, Q):
    z = 0 

    if (P == z):
        return Q
    if (Q == z):
        return P

    if P[0] == Q[0]:
        if (P == (Q[0], -Q[1] % p)):
            return z
        else:
            m = ((3*pow(P[0], 2, p) + A)*pow(2*P[1], p-2, p)) % p
    else:
        m = (P[1] - Q[1])*pow(P[0] - Q[0], p-2, p) % p

    x = (pow(m, 2, p) - P[0] - Q[0]) % p
    y = (m*(P[0] - x) - P[1]) % p
    return (x, y)

#Run Tests
# points = generate_points(2, 1, 5)
# point = (0, 1)
# print(scalar_multipliation(2, 1, 5, 2, point))

# print(addition(1, 6, 11, (2, 4), (5, 9)))
# print(addition(1, 6, 11, (2, 4), (2, 4)))