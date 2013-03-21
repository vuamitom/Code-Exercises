"""
Given N numbers [N<=10^5], count the total pairs of numbers that have a difference of K. [K>0 and K<1e9]. Each of the N numbers will be > 0 and be less than K away from 2^31-1 (Everything can be done with 32 bit integers).
"""
from math import fabs
def count_pairs(seq, K):
    count = 0
    for i, j in ((i,j) for ix, i in seq for jx, j in seq if jx > ix ): 
        #print (str(i) + " " + str(j))
        if fabs(i - j) == K : 
            #print ("--- " + str(i) + " " + str(j))
            count+= 1
    return count


if __name__ == "__main__":
    N, K = [ int(x) for x in raw_input('').split(' ') ]
    seq = [int (x) for x in raw_input('').split(' ')]
    print(str(count_pairs(seq, K)))

