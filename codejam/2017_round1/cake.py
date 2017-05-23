

def solve(nr, nc, cake):
    # print nr 
    # print nc
    done = set()
    for r in xrange(0, nr):
        for c in xrange(0, nc):
            if not cake[r][c] == '?' and cake[r][c] not in done:
                l = cake[r][c]
                sr, sc = r, c
                er, ec = r, c
                while sc >= 0 and (cake[sr][sc] == '?' or cake[sr][sc] == l):
                    sc -= 1
                sc +=1      

                while ec < nc and (cake[er][ec] == '?' or cake[er][ec] == l):
                    # print ec
                    # print cake[er]
                    ec += 1
                ec -= 1
                cr = sr - 1
                while cr >=0:    
                    ok = True            
                    for t in xrange(sc, ec+1):
                        if not cake[cr][t] == '?' and not cake[cr][t] == l:
                            ok = False
                            break
                    if ok:
                        sr = cr
                        cr -= 1
                    else:
                        break
                cr = er + 1
                while cr < nr:
                    ok =True
                    # print 'cr = ' + str(cr)            
                    for t in xrange(sc, ec + 1):
                        if not cake[cr][t] == '?' and not cake[cr][t] == l:
                            ok = False
                            break
                    if ok:
                        er = cr
                        cr += 1
                    else:
                        break
                # print 'range: ' + str(sr) + ' ' + str(sc) + ' ' + str(er) + ' ' + str(ec)
                # print 'BEFORE: ' + str(cake)
                for t in xrange(sr, er+1): 
                    # print 'l1 = ' + str(cake[t])                   
                    cake[t] = cake[t][0:(sc)] + (l * (ec - sc + 1)) + cake[t][(ec + 1):]
                    # print 'l2 = ' + str(cake)
                # print 'AFTER: ' + str(cake)
                    # for v in xrange(sc, ec+1):
                    #     cake[t][v] = l                
                done.add(l)
    for r in xrange(0, nr):
        print cake[r]


t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    r, c = [int(x) for x in raw_input().split(' ')]
    cake = []
    for j in xrange(0, r):
        cake.append(raw_input())
    print 'Case #' + str(i) + ':'
    solve(r, c, cake)