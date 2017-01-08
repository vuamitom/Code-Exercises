import math
def pr(i, r):
    print 'Case #' + str(i + 1) + ': ' + ('black' if r == 1 else 'white')

def solve():
    n = int(raw_input())
    #print 'n = ' + str(n)
    for i in range (0, n):
        p, x, y = [int(z) for z in raw_input().split()]
        if p == 0:
            pr(i, 0)
            continue 
        d = ((x - 50) ** 2 + (y - 50) ** 2) ** 0.5 
        if d > 50:
            pr(i, 0)
        else:
            #t = (x - 50) / (y - 50)
            a = math.atan2(x - 50,y - 50)
            if a < 0:
                a = 2* math.pi +  a
            a = a * (360 / (2 * math.pi))
            #print 'a = ' + str(a) + ' p = ' + str(p * 360 / 100)
            pr(i, 1 if a <= (p * 360 / 100) else 0)
        
if __name__ == '__main__':
    solve()
