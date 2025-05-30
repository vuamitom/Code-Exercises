#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'legoBlocks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER m
#

rowConfig = []
blocks = [1,2,3,4]
based = 10**9 + 7
cached = dict()

def legoRow(m):
    # different ways of arranging a row
    if m < len(rowConfig):
        return rowConfig[m]
    for i in range(0, m + 1):
        if i >= len(rowConfig):
            rowConfig.append(0)
            
        if i == 0:
            rowConfig[i] = 0 
        elif rowConfig[i] == 0:
            perm = 0
            for b in blocks:
                if i - b >=0:
                    perm += rowConfig[i-b] if rowConfig[i - b] > 0 else 1 
            rowConfig[i] = perm 
    return rowConfig[m] 
     

def calLegoBlock(n, m):
    if (n, m) in cached:
        return cached[(n, m)]        
    
    blocks = [0] * m 
    alls =[0] * m 
    for i in range(m):
        alls[i] = pow(legoRow(i + 1), n, based)

    for i in range(m):        
        blocks[i] = alls[i]
        
        for j in range (1, i+1):
            verticals = (alls[j - 1] * blocks[i - j]) % based 
            blocks[i] = (blocks[i] - verticals) % based 
    return blocks[m-1]
    
    # total = rowPerm**n 
    # # print('total perm ', total)
    # for i in range(1, m):
    #     print('i = ', i)
    #     verticals = (legoRow(i) ** n) * calLegoBlock (n, m - i)
    #     total = total - verticals 
        
    # print('total valid perm ', total)
    # return total 

def legoBlocks(n, m):
    # Write your code here
    total = calLegoBlock(n, m)
    cached[(n, m)] = total
    return total  
    # return total % based

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        result = legoBlocks(n, m)

        fptr.write(str(result) + '\n')

    fptr.close()
