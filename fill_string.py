import time
def tamvm(n, c):
    r = '' 
    while n > 0:
        if n & 1: 
            r += c 
        n >>= 1
        if n: 
            c += c
    return r

def tamvm2(n, c):
    r = ''
    for i in xrange(0, n): 
        r += c 
    return r 

def quangna(n, c):
    # return ''.join([c] * n)
    r = []
    while n > 0: 
        r.append(c)
        n -= 1
    return ''.join(r)
def longdt(n, c):
    return c*n

def benchmark(m):
    start = time.time()
    for i in xrange(0,10):
        m(100000000, 'c')
    end = time.time()
    return end-start

#ms = [('quangna', quangna), ('longdt', longdt), ('tamvm',tamvm), ('tamvm2', tamvm2)]
#for p in ms:
#    n, m = p
#    t = benchmark(m)
#    print n + ': ' +str(t)
print benchmark(quangna)
