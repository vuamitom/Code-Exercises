def solve(N, G, K):
    return check(1, 0, N, G, K, [0] * K)

def check(n, p, N, G, K, d):
    adj = G[n]
    c = 100000000
    d [n -1] += 1
    done = True
    for i in range(0, len(d)):
        if d[i] == 0:
            done = False
            break
    if n == len(G):
        return p

    while len(adj) > 0:
        if not done:
            nc = []
            for i in range(0, len(adj)):
                n2, _ = adj[i]
                t = N[n2]
                if d[t] == 0:
                    nc.append(i)
            if len(nc) == 0:
                m = 0
                for i in range(0, len(adj)):
                    m = i if adj[i][1] < adj[m][1] else m
                p2 = p + adj[m][1]
                if p2 >= c:
                    adj.pop(m)
                    break

                c2 = check(adj[m][0], p2, N, G, K, d)
                d[adj[m][1]] -= 1
                c = c2 if c2 < c else c
                adj.pop(m)
            else:
                m = 0
                for i in range(0, len(nc)):
                    m = nc[i] if adj[nc[i]][1] < adj[m][1] else m
                p2 = p + adj[m][1]
                if p2 >= c:
                    adj.pop(m)
                    break
                c2 = check(adj[m][0], p2, N, G, K, d)
                d[adj[m][1]] -= 1
                c = c2 if c2 < c else c
                adj.pop(m)
        else:
            m = 0
            for i in range(0, len(adj)):
                m = i if adj[i][1] < adj[m][1] else m
                if adj[i] == len(G):
                    return p + adj[i][1]
            p2 = p + adj[m][1]
            if p2 >= c:
                adj.pop(m)
                break
            c2 = check(adj[m][0], p2, N, G, K, d)
            d[adj[m][1]] -= 1
            c = c2 if c2 < c else c
            adj.pop(m)
    return c


if __name__ == '__main__':
    N = { a: a for a in range(1,6)}
    G = [[(2, 10), (3, 10)], [(1, 10), (4, 10)], [(1, 10), (5, 10)], [(2, 10), (5, 10)], [(3, 10), (4, 10)]]
    r = solve(N, G, 5)
    print 'solved = '.r
