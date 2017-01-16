import math

def solve():
    t = int(raw_input())
    for d in range(0, t):
        n = int(raw_input())
        w = [int(raw_input()) for j in range(0, n)]
        w.sort()
        c = 0
        x, y = 0, len(w) - 1
        while ( x <= y ):
            top = w[y]
            no = int(math.ceil(50.0 / top))
            if y - x + 1 >= no:
                c += 1
            else:
                break
            y -= 1
            x += (no - 1)
        print 'Case #' + str(d + 1) + ': ' + str(c)
solve()

