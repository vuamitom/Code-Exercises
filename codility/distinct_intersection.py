# -*- encoding: utf-8 -*-
"""
We draw N discs on a plane. The discs are numbered from 0 to N − 1. A zero-indexed array A of N non-negative integers, specifying the radiuses of the discs, is given. The J-th disc is drawn with its center at (J, 0) and radius A[J].

We say that the J-th disc and K-th disc intersect if J ≠ K and the J-th and K-th discs have at least one common point (assuming that the discs contain their borders).

The figure below shows discs drawn for N = 6 and A as follows:

  A[0] = 1
  A[1] = 5
  A[2] = 2
  A[3] = 1
  A[4] = 4
  A[5] = 0


There are eleven (unordered) pairs of discs that intersect, namely:

discs 1 and 4 intersect, and both intersect with all the other discs;
disc 2 also intersects with discs 0 and 3.
Write a function:

def solution(A)

that, given an array A describing N discs as explained above, returns the number of (unordered) pairs of intersecting discs. The function should return −1 if the number of intersecting pairs exceeds 10,000,000.

Given array A shown above, the function should return 11, as explained above.

Assume that:

N is an integer within the range [0..100,000];
each element of array A is an integer within the range [0..2,147,483,647].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

# you can use print for debugging purposes, e.g.
# print "this is a debug message"

def solution(A):
    # write your code in Python 2.7
    seg = [ (i-v, i + v) for i, v in enumerate(A)] 
    seg.sort(key=lambda a: a[0])
    c = 0 
    #print seg
    for i, n in enumerate(seg): 
        b, e = n
        #for j in xrange(i+1, len(seg)): 
        #    if seg[j][0] > e:
        #        break 
        #    elif b <= seg[j][0] <= e: 
        #        c += 1
        #        if c > 10000000:
        #            return -1
        last = binary_check(e, i+1, len(seg)-1, seg)
        #print last 
        c += last - i 
        #print 'c = ' + str(c)
        if c > 10000000:
            return -1 
    return c
#t = 0 
def binary_check(needle, b, e, ar): 
    #print 'b = ' + str(b) + ' e = ' + str(e)
    #global t 
    if b >= e: 
        return e if ar[e][0] <= needle else e -1 
    if ar[b][0] > needle: 
        return b-1
    m =( e - b ) >> 1 
    m = m + b
    #print 'm+ = ' + str(m) 
    if ar[m][0] <= needle:
        return binary_check(needle, m + 1, e, ar)
    elif ar[m][0] > needle: 
        return binary_check(needle, b, m-1,  ar) 


print solution([1, 5, 2, 1, 4, 0])
