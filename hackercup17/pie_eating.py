def solve_sub(M, m):
    temp = []
    for r in range(0, len(M)):
        p = None if r == 0 else temp[r -1]
        d = [0] * (min(len(d), (r + 1) * m))
        c = M[r]
        for o in range(0, min(len(d), (r + 1) * m)):
            if not p:
                if o > 0:
                    d[o] = sum(c[:(o + 1)]) + (o + 1) ** 2
                else:
                    d[o] = c[o] + 1
            else:
                if o < r:
                    d[o] = p[o]
                else: 
                    d[o] = min([p[o-1] + min(c) + 1, p[o]]) if o < len(p) else p[len(p) - 1] + sum(c[0:(o - len(p) + 1)]) + (o - len(p) + 1) ** 2
        temp.append(d)
    print temp
    l = temp[len(temp) - 1][len(M) - 1]
    return l

        


def solve():
    t = int(raw_input())
    for r in range(0, t):
        n, m = [int(x) for x in raw_input().split(' ')]
        M = [sorted([int(x) for x in raw_input().split(' ')]) for y in range(0, n)]
        r2 = solve_sub(M, m)
        print 'Case #'+ str(r + 1) + ': ' +  str(r2)
solve()
