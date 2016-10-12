#!/bin/python

import sys


Q = int(raw_input().strip())
for a0 in xrange(Q):
    n = int(raw_input().strip())
    b = raw_input().strip()
    t = [0] * 27
    happy = True
    for i, c in enumerate(b):
        if c == '_':
            t[26] += 1
        else:
            t[ord(c) - 65] += 1
        if (i == 0 or not b[i-1] == c) and (i == len(b)-1 or not b[i+1] == c):
            happy = False
    if (sum([1 for i in t[:-1] if i == 1 ]) > 0):
        print 'NO'
    elif t[26] > 0:
        print 'YES'
    else:
        print 'NO' if not happy else 'YES'
