# -*- encoding: utf-8 -*-
"""
A non-empty zero-indexed array A consisting of N integers is given. The product of triplet (P, Q, R) equates to A[P] * A[Q] * A[R] (0 ≤ P < Q < R < N).
  A[0] = -3
  A[1] = 1
  A[2] = 2
  A[3] = -2
  A[4] = 5
  A[5] = 6
contains the following example triplets:

(0, 1, 2), product is −3 * 1 * 2 = −6
(1, 2, 4), product is 1 * 2 * 5 = 10
(2, 4, 5), product is 2 * 5 * 6 = 60
Your goal is to find the maximal product of any triplet.

Write a function:

def solution(A)

that, given a non-empty zero-indexed array A, returns the value of the maximal product of any triplet.

For example, given array A such that:

  A[0] = -3
  A[1] = 1
  A[2] = 2
  A[3] = -2
  A[4] = 5
  A[5] = 6
the function should return 60, as the product of triplet (2, 4, 5) is maximal.

Assume that:

N is an integer within the range [3..100,000];
each element of array A is an integer within the range [−1,000..1,000].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


# you can use print for debugging purposes, e.g.
# print "this is a debug message"

def solution(A):
    # write your code in Python 2.7
    small = [-1, -1]
    large = [-1, -1, -1]
    for i, n in enumerate(A): 
        put_large(A, large, i)
        put_small(A, small, i) 
    m, lg = -1, -2000
    for idx in large:
        if A[idx] > lg:
            m = idx 
            lg = A[idx]
    small.append(m)

    p1 = reduce(lambda x, y: x * A[y], small, 1)
    p2 = reduce(lambda x, y: x * A[y], large, 1)
    return p1 if p1 > p2 else p2

def put_large(A, ls, i):
    m, smallest = -1, None   
    for c, n in enumerate(ls): 
         if n < 0: 
             smallest = -2000
             m = c 
             break 

         if not smallest or smallest > A[n]: 
             m = c 
             smallest = A[n] 
    if smallest <  A[i]: 
        ls[m] = i 

def put_small(A, ls, i): 
    m, largest = -1, None   
    for c, n in enumerate(ls):
         if n < 0: 
             largest = 2000
             m = c 
             break 
              
         if not largest or largest < A[n]: 
             m = c
             largest =A[n] 
    if largest >  A[i]: 
        ls[m] = i
    
    
print solution([-3, 1, 2, -2, 5, 6]) 
