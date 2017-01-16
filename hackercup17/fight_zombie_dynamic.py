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
    m = []
    p = 1 / ( y * 1.0)
    for i in range(1, x + 1):
        n = [0] * (x * y)
        for j in range(1, x * y + 1):
            if i == 1: 
                if j > y: 
                    break
                else:
                    n[j - 1] = p
            else:
                s = 0
                for z in range(j - y, j):
                    if z >= 0:
                        s += m[i - 2][z - 1] * p
                n[j - 1] = s
        m.append(n)
    # print m
    r = sum (m[x-1][d-1:])
    return r 

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
