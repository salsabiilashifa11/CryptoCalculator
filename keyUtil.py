
def saveKeyRSA(e, n, d, path):
    public = open(path+".pub", 'w')
    public.write(str(e)+ " " + str(n))
    public.close()
    private = open(path+".pri", 'w')
    private.write(str(d) + ' ' + str(n))
    private.close()

def loadPublicRSA(path):
    f = open(path, 'r')
    public = f.read().split(' ')
    f.close()
    e = int(public[0])
    n = int(public[1])

    return e,n

def loadPrivateRSA(path):
    f = open(path, 'r')
    private = f.read().split(' ')
    f.close()
    d = int(private[0])
    n = int(private[1])

    return d,n

def saveKeyPaillier(n, g, m, l, path):
    public = open(path+".pub", 'w')
    public.write(str(g)+ " " + str(n))
    public.close()
    private = open(path+".pri", 'w')
    private.write(str(l) + ' ' + str(m) + ' ' + str(n))
    private.close()

def loadPublicPaillier(path):
    f = open(path, 'r')
    public = f.read().split(' ')
    f.close()
    g = int(public[0])
    n = int(public[1])

    return g,n

def loadPrivatePaillier(path):
    f = open(path, 'r')
    private = f.read().split(' ')
    f.close()
    l = int(private[0])
    m = int(private[1])

    return l,m