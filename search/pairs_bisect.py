"""
Given N numbers [N<=10^5], count the total pairs of numbers that have a difference of K. [K>0 and K<1e9]. Each of the N numbers will be > 0 and be less than K away from 2^31-1 (Everything can be done with 32 bit integers).
"""
from bisect import insort
def next(seq):
    start = 0
    idx = 0
    for idx, char in enumerate(seq):
        if char == ' ':
            if idx > start: 
                yield(int(seq[start:idx]))
                start = idx + 1

    if start < len(seq):
        yield(int(seq[start: len(seq)]))
        

if __name__ == "__main__":
    N, K = [ int(x) for x in raw_input('').split(' ') ]
    line = raw_input('')
    numbers = list()
    #insert in a sorted list 
    for  x in list(next(line)):
       insort(numbers, x) 

    #print numbers
    #count pairs 
    count = 0
    for idx, x in enumerate(numbers):
        for n in numbers[(idx+1):N]:
            if n - x == K:
                count += 1
            elif n - x > K:
                break;

    print count
        
    
