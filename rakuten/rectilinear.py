# you can use print for debugging purposes, e.g.
# print "this is a debug message"

def is_overlap(K, L, M, N, P, Q, R, S):
    if R < K or M < P:
        return False 
    if S < L or Q > N:
        return False 
    return True

def overlap(K, L, M, N , P, Q, R, S): 
    if not is_overlap(K, L, M, N, P, Q, R, S): 
        return 0
    x = max(0, min(M, R) - max(K, P))
    y = max(0, min(N, S) - max(L, Q))
    return x * y

def area(Lx, Ly, Rx, Ry):
    return (Rx-Lx) * (Ry-Ly)

def solution(K, L, M, N, P, Q, R, S):
    # write your code in Python 2.7
    a1 = area(K, L, M, N)
    a2 = area(P, Q, R, S)
    r = a1 + a2 - overlap(K, L, M, N, P, Q, R, S)
    print r
    return r  if r <= 2147483647 else -1

print solution(0, 0, 1, 1, 3, 1, 4, 3)
print solution(-40000, 10000, 20000, 60000, 0, -10000, 40000, 30000)
     
