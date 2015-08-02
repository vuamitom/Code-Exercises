"""
A non-empty zero-indexed array A consisting of N integers is given. A pair of integers (P, Q), such that 0 ≤ P < Q < N, is called a slice of array A (notice that the slice contains at least two elements). The average of a slice (P, Q) is the sum of A[P] + A[P + 1] + ... + A[Q] divided by the length of the slice. To be precise, the average equals (A[P] + A[P + 1] + ... + A[Q]) / (Q − P + 1).
For example, array A such that:
    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8
contains the following example slices:
slice (1, 2), whose average is (2 + 2) / 2 = 2;
slice (3, 4), whose average is (5 + 1) / 2 = 3;
slice (1, 4), whose average is (2 + 2 + 5 + 1) / 4 = 2.5.
The goal is to find the starting position of a slice whose average is minimal.
Write a function:
def solution(A)
that, given a non-empty zero-indexed array A consisting of N integers, returns the starting position of the slice with the minimal average. If there is more than one slice with a minimal average, you should return the smallest starting position of such a slice.
For example, given array A such that:
    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8
the function should return 1, as explained above.
Assume that:
N is an integer within the range [2..100,000];
each element of array A is an integer within the range [−10,000..10,000].
Complexity:
expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
Copyright 2009–2015 by Codility Limited. All Rights Reserved. Unauthorized copying, publication or disclosure prohibited.
"""
# you can use print for debugging purposes, e.g.
# print "this is a debug message"

def solution(A):
    # write your code in Python 2.7
    min_avg = None 
    max_end = None
    
    for i in xrange(1, len(A)):
        # find min avg. slice that ending at i 
        s = A[i]+ A[i-1]
        if not max_end:            
            max_end = (i-1, i, s, s/2.0)
        else:
            max_end = (max_end[0], i, max_end[2] + A[i], (max_end[2] + A[i])/float(i - max_end[0]+ 1))
            if s/2 < max_end[3]:
                max_end = (i-1, i, s, s/2.0)        
        if not min_avg:
            min_avg = max_end 
        else: 
            c = min_avg[3]
            e = max_end[3] 
            if e < c: 
                min_avg = max_end     
    return min_avg[0]
