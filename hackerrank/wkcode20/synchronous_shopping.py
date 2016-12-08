import itertools
g = 0
def solve(N, G, K):
    return check(1, 0, N, G, K, [0] * K)

def sp(s, G, g):
    adj = G[s -1]
    q = [(s, 0)]
    while len(q) > 0:
        m = 0
        for i in range(0, len(q)):
            m = i if q[i][1] < q[m][1] else m
        t = q[m]
        q.pop(m)
        n, d = t
        if n == g:
            return d
        adj = G[n - 1]
        for i in range(0, len(adj)):
            n2, d2 = adj[i]
            d2 = d2 + d
            f = False
            for j in range(0, len(q)):
                if q[j][0] == n2:
                    f = True
                    if q[j][1] > d2:
                        q[j] = (n2, d2)
                    break
            if not f:
                q.append((n2, d2))
    return 1000000

cur = 1000000
def check(n, p, N, G, K, d):
    global g
    global cur
    g += 1
    #if g > 40: return p
    print 'visiting '+str(n) + ' d = ' + str(p)
    adj = list(G[n-1])
    c = cur 
    d [n -1] += 1
    #print 'dd == ' + str(d)
    done = True
    for i in range(0, len(d)):
        if d[i] == 0:
            done = False
            break
    if done and n == len(G):
        return p
     
    #print 'ddi0 == ' + str(d)
    while len(adj) > 0:
        if not done:
            #print 'ddi2 == ' + str(d)
            nc = []
            for i in range(0, len(adj)):
                n2, _ = adj[i]
                t = N[n2]
                if d[t-1] == 0:
                    nc.append(i)
            #print 'adj = ' + str(adj) + ' nc = '  + str(nc) + ' d = ' + str(d)
            if len(nc) == 0:
                m = 0
                for i in range(0, len(adj)):
                    m = i if adj[i][1] < adj[m][1] else m
                p2 = p + adj[m][1]
                #print 'cur = ' + str(c) + ' nex = ' + str(p2)
                if p2 >= c:
                    adj.pop(m)
                    print 'too bad, already found better'
                    break

                c2 = check(adj[m][0], p2, N, G, K, d)
                d[adj[m][0] - 1] -= 1
                c = c2 if c2 < c else c
                adj.pop(m)
            else:
                m = nc[0]
                for i in range(0, len(nc)):
                    m = nc[i] if adj[nc[i]][1] < adj[m][1] else m
                p2 = p + adj[m][1]
                if p2 >= c:
                    adj.pop(m)
                    break
                c2 = check(adj[m][0], p2, N, G, K, d)
                d[adj[m][0] - 1] -= 1
                c = c2 if c2 < c else c
                adj.pop(m)
        else:
            #m = 0
            #for i in range(0, len(adj)):
            #    m = i if adj[i][1] < adj[m][1] else m
            #    if adj[i] == len(G):
            #        return p + adj[i][1]
            #print 'done: adj = ' + str(adj) + ' d = ' + str(d)
            #p2 = p + adj[m][1]
            #if p2 >= c:
            #    adj.pop(m)
            #    break
            #c2 = check(adj[m][0], p2, N, G, K, d)
            #d[adj[m][1]] -= 1
            #c = c2 if c2 < c else c
            #adj.pop(m)
            pp = sp(n, G, len(G))
            c2 = p + pp
            cur = c2 if c2 < cur else cur
            print 'done at: ' + str(c2)
            return c2 
    #print 'return : ' + str(c)
    return c


if __name__ == '__main__':
    K = 5
    T = range(1, K + 1)
    G = [[(2, 10), (3, 10)], [(1, 10), (4, 10)], [(1, 10), (5, 10)], [(2, 10), (5, 10)], [(3, 10), (4, 10)]]
    N = { a: a for a in range(1,6)}    
    m = 10000000
    for i in range(1, (K/2) + 1):
        for t in itertools.combinations(T, i):
            t2 = [x for x in T if x not in t]
            d1 = solve(N, G, 5)
            d2 = solve(N, G, 5)
            d = d1 if d1 > d2 else d2
            m = d if d < m else m
    print 'solve m = ' + str(m)
