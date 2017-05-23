import sys
hex = sys.argv[1]
htob = {
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15
}
res = []
for i in range(0, len(hex), 2):
    a = 0
    for j in range(0, 2):        
        c = hex[i + j]
        j = 1 - j
        if c in htob:
            a |= (htob[c] << (4 * j))
        else:
            a |= int(c) << (4 * j)
    # print hex[i:i +2]
    # print a
    res.append(a)

# to base64
print res
r = 0
output = []
for i, b in enumerate(res):
    o = 0
    if r > 0:
        o = (res[i - 1]  & (0xff >> (8 - r))) << r
    print b
    # o |= ((b &  (0xff >> (r + 2) )) << r)
    o |= (b & (0xff & ~(0xff >> (r + 2)))) >> r + 2
    print o
    output.append(chr(o))
    r = r + 2
    r = 0 if r == 8 else r
    if i == len(res) - 1 and r > 0:
        if r == 2:
            output.append('=')
            output.append('=')
        else:
            output.append('=')
print ''.join(output)
        



 
