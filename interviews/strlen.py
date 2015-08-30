"""
Implement string comparison strcmp. What happen if you don't have strlen (I used C++)?
"""

def strcmp(a, b): 
    for idx, c in enumerate(a): 
        c2 = None if idx >= len(b) else b[idx]
        if c2 is None or c > c2: 
            return 1
        elif c < c2:
            return -1
    if len(b) > len(a): 
        return -1
    else:
        return 0



assert(strcmp("abc","abc") ==  0)
assert(strcmp("abc","abcd") ==  -1)
assert(strcmp("abce","abc") ==  1)
assert(strcmp("fbce","abc") ==  1)
assert(strcmp("abce","xbc") ==  -1)
