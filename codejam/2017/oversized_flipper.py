
def solve(s, k):
    ls = list(s)
    n = 0
    for i in xrange(0, len(ls) - k + 1):
        # print i
        c = ls[i]
        if c == '-':
            for j in xrange(i, i + 1 + k - 1):
                ls[j] = '-' if ls[j] == '+' else '+'
            n += 1
        if i == len(ls) - k:
            # print ls
            if ''.join(ls[i:len(ls)]) == '+' * k:
                # print 'test1'
                return str(n)                    
            else:
                # print 'test2'
                return 'IMPOSSIBLE'

def test():
    assert solve('---+-++-', 3) == '3'
    assert solve('+++++', 4) == '0'
    assert solve('-+-+-', 4) == 'IMPOSSIBLE'
    assert solve('-+-+-', 3) == '3'

t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    s, k = raw_input().split(" ")
    k = int(k)
    print 'Case #' + str(i) + ': ' + solve(s, k)
# test()
    

