import sys

def can_win(w, b, m):
    bq = None 
    bo = [[0] * 4] * 4
    for p in b:
        t, c, r = p
        if t == 'Q':
            bq = (c, r)
        bo[r][c] = 'b' + t

    for p in w:
        t, c, r = p
        bo[r][c] = t

    for p in w:
        t, c, r= p
        if t == 'Q':
            if c == bq[0]:
                s, e = min(c, bq[0]), max(c, bq[0])
                if 
                

    

g = int(raw_input().strip())
for c in range(0, g):
    w, b, m = [int(t) for t in raw_input().strip().split(' ')]
    wh = []
    bh = []
    for wc in range(0, w):
        t, c, r = [p for p in raw_input().strip().split(' ')]
        r = int(r)
        c = ord(c) - 65
        wh.append((t, c, r))
    for bc in range(0, b):
        t, c, r = [p for p in raw_input().strip().split(' ')]
        r = int(r)
        c = ord(c) - 65
        bh.append((t, c, r))

    if can_win(w, b, m):
        print 'YES'
    else:
        print 'NO'
