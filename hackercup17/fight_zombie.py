import math
import re
def pad(s):
    return s + ('0'*(6 - len(s) + s.find('.') + 1))
def ps(x, y, c):
    m  = 1
    for i in range (x - c + 1, x + 1):
        m *= i
    return m*1.0 * ((y - 1)** (x -c)) / math.factorial(c) / (y ** x) 

def cal(x, y, d):
    #print 'cal ' + str(x) + ' ' + str(y) + ' ' + str(d)
    if d <= x or d == 0:
        #print 'ret'
        return 1
    elif d > ( y * x ):
        return 0
    else:
        s = 0
        for i in range (1, x + 1):
            r = ps ( x, y , i ) * cal ( x- i, y - 1, d - (y * i)) 
            #print 'r = ' + str(r) + ' for ' + str(i) + ' of ' + str(y)
            s += r
        s += cal ( x, y - 1, d) * (( (y - 1) / (y * 1.0)) ** x )
        return s

def solve():
    n = int(raw_input())
    for i in range (0, n):
        d, s = [int(x) for x in raw_input().split()]
        sp = [x for x in raw_input().split()]
        m = 0 
        for p in sp:
            tk = [int(z) for z in re.split(r'[d+-]', p)]
            x, y = tk[:2]
            z = tk[2] if len(tk) == 3 else 0
            z = 0 - z if p.find('-') >= 0 else z 
            x, y, z = int(x), int(y), int(z)
            ps = cal(x, y, d - z)
            m = ps if ps > m else m
        print 'Case #' + str(i + 1) + ': ' + pad(str(round(m, 6)))

solve()
