def solve(n):
    s = [int(c) for c in list(str(n))]
    i = len(s) - 1
    while i >= 1:
        j = i - 1
        d = s[i]
        b = s[j]
        if d < b:            
            b = b - 1                              
            while b < 0:                
                b = 9
                s[j] = b
                j -= 1
                b = s[j] - 1                    
            s[j] = b
            for z in range (i, len(s)):
                if s[z] < 9:
                    s[z] = 9                                        
                else: 
                    break
        i -= 1
    s = ''.join([str(c) for c in (s if int(s[0]) > 0 else s[1:])])
    # print s
    return s

def test():
    assert solve('132') == '129'
    assert solve('1327') == '1299'
    assert solve('13277') == '12999'
    assert solve('1000') == '999'
    assert solve('7') == '7'
    assert solve('111111111111111110') == '99999999999999999'
    assert solve('999990') == '899999'
    assert solve('789') == '789'
    assert solve('19999') == '19999'
    assert solve('912') == '899'
    assert solve('909') == '899'
    assert solve('172') == '169'
    assert solve('132000098') == '129999999'
    assert solve('0') == '0'
    assert solve('1')
    assert solve('987656789') == '899999999'

test()
t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    n = raw_input()
    print 'Case #' + str(i) + ': ' + solve(n)