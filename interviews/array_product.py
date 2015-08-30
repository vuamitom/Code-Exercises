"""
Given an array A[1..n], Compute B[1..n] that B[i] is the product of all element in A except A[i]. Find a solution not using division (/)
"""

def array_product(A): 
    B = [0] * len(A)
    Z = [0] * len(A)
    C = [0] * len(A)
    p = 1
    for i, a in enumerate(A): 
        p = p * a 
        Z[i] = p

    p = 1 
    for i in xrange(0, len(A)): 
        p = p * A[len(A) - i - 1]
        C[len(A) -i - 1] = p

    for i in xrange(0, len(A)):
        p1 = 1 if i == 0 else Z[i-1]
        p2 = 1 if i == len(A)-1 else C[i+1]
        B[i] = p1 * p2 

    return B


A = [ 1, 5, 3, 6, 8 , 10]
B = array_product(A)
print B
p = reduce(lambda a, x: a * x, A, 1)
for i, v in enumerate(B):
    assert(B[i] == p / A[i])
