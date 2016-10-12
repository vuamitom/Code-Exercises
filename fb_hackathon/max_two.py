#!/bin/python

import sys
import os


def max_two(arr):
    m1, m2, ma = None, None, None 
    L, R = None, None
    for i in range(0, len(arr)):
        m1, m2 = None, None
        for j in range(i, len(arr)):
            old_m1 = m1
            if m1 is None or m1 < arr[j]: 
                m2 = m1 
                m1 = arr[j]
            elif (m2 is None or m2 < arr[j]):
                m2 = arr[j]
            print str(m1) + " " + str(m2) + " " + str(i) + " " + str(j)
            if m1 is not None and m2 is not None:
                t = m1 & m2 
                if ma is None or t > ma: 
                    ma = t
                    L = i
                    R = j 
    return L, R



_arr_cnt = 0
_arr_cnt = int(raw_input())
_arr_i=0
_arr = []
while _arr_i < _arr_cnt:
    _arr_item = int(raw_input());
    _arr.append(_arr_item)
    _arr_i+=1
    

res = max_two(_arr);
print res 
