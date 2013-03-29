"""
Queens have always hated each other. Traditionally when queens were placed on a chessboard a queen gets jealous of another if:

They are both in the same row.
They are both in the same column.
They can see each other diagonally i.e lie in a line inclined 45 degrees or 135 degrees to the base of board.
But now the hatred has increased and the new condition is that no three of them should lie in any straight line (this line need not be aligned 45 degrees or 135 degrees to the base of chess board).
"""
result = [] # this serves mainly as an index to avoid iteration
cache = dict()
from random import randint
def insert(r,N,b):
    """ insert a queen into row r of board b """ 
    #start = 0 if r > 0 else 1
    #avail = space - result
    avail = [x for x in space if x not in result]
    #for c in range ( N):
    while len(avail) > 0:
        indx = randint(0, len(avail) - 1)
        c = avail[indx]
        del avail[indx]
        #insert queen in col c for row r 
        if(b[r][c] == 0):
            #b[r][c] = 1
            result.append(c)
            #cross_row(r,b) - we don't actually need to call this
            if r < (N-1):
                cross_col(r + 1, c, N, b)
                cross_diagon((r , c), N, b)
                drop = cross_line((r, c), N , b)
                if(insert( r + 1, N , b)):
                    return True  
                else: 
                    # unroll the operations - go for this instead of keeping a copy of the matrix
                    uncross_col( r + 1, c, N , b)
                    uncross_diagon((r, c), N , b)
                    for (y,x) in drop:
                        b[y][x] +=1 
                    result.pop()
            else:
                return True
    return False 

    

def cross_row(r, b):
    """ don't need this """ 

def cross_col(start, c, N,  b):
    """ cross out column c from row 'start' """ 
    for r in range (start, N):
        b[r][c] -= 1

def uncross_row (r, b):
    """ don't need this """ 

def uncross_col (start, c, N,  b):
    """ un mark column c from row 'start' """
    for r in range (start, N):
        b[r][c] += 1

def cross_line( p,N, b ):
    """ TODO """
    #draw a line from the rest to this point, and cross out the board
    x = p[0]
    y = p[1]
    drop = []
    for  r, c in enumerate(result[:-1]):
        #for c in range (N):
        #if b[r][c] == 1:
        dx = x - r
        dy = y - c
        (dx, dy) = get_slope(dx, dy)
        r2 = x + dx
        c2 = y + dy 
        while ( r2 < N and c2 < N and c2 >= 0 ):
            b[r2][c2] -= 1
            drop.append((r2,c2))
            r2 += dx 
            c2 += dy
    return drop

def uncross_line (p,N, b):
    """ TODO """
    x = p[0]
    y = p[1]
    for r , c in enumerate(result[:-1]) :
        #for c in range(N):
        #if b[r][c] == 1:
        dx = x - r 
        dy = y - c
        (dx, dy) = get_slope(dx, dy)
        r2 = x + dx 
        c2 = y + dy
        while r2 < N and c2 < N and c2 >= 0 : 
            b[r2][c2] += 1
            r2 += dx
            c2 += dy

def cross_diagon (p, N,  b):
    """ cross out diagon from point p """ 
    x = p[0] + 1
    y = p[1] + 1
    while ( x < N and y < N ):
        b[x][y] -= 1
        x += 1
        y += 1
    x = p[0] + 1
    y = p[1] - 1
    while ( x < N and y >= 0):
        b[x][y] -= 1
        x += 1
        y -= 1

def mem_cache(fn):
    """mem_cache"""
    def wrapper(x,y):
        absx = abs(x) 
        absy = abs(y)
        if(absx < absy):
            res = cache.get((absx, absy),None)
            if res is not None:
                return (res[0]*x/absx, res[1]*y/absy)
            else:
                res = fn(x,y)
                cache[(absx,absy)] = (abs(res[0]),abs(res[1]))
                return res
        else:
            res = cache.get((absy, absx),None)
            if res is not None:
                return (res[1]*x/absx, res[0]*y/absy)
            else:
                res = fn(x, y)
                cache[(absy, absx)] = (abs(res[1]), abs(res[0])) 
                return res
    return wrapper
        
@mem_cache
def get_slope(dx, dy):
    """get slope """
    #for i in reversed(range(2, n+1)):
    p = 0
    i = primes[p]
    while i <= abs(dx) and i <= abs(dy):
        while dx % i == 0 and dy %i == 0:
            dx /= i
            dy /= i
        p += 1
        if p >= len(primes):
            break
        i = primes[p]
    return (dx, dy)

def print_result(b):
    """ print result """ 
    #res = ""
    #for r in range (N):
    #    for c in range (N):
    #        if b[r][c] == 1: 
    #            res += str(c + 1) + " " 
    #print result
    print ' '.join(str(n + 1) for n in result)

def print_verbose(b):
    for r in range (N):
        row = ""
        for c in range (N):
            char = "Q" if b[r][c] == 1 else "*"
            row += char
        print row 

def uncross_diagon (p,N, b):
    x = p[0] + 1
    y = p[1] + 1
    while ( x < N and y < N ) : 
        b[x][y] += 1
        x += 1 
        y += 1
    x = p[0] + 1
    y = p[1] - 1
    while ( x < N and y >= 0):
        b[x][y] += 1
        x += 1
        y -= 1
import time
def profile(fn):
    def with_profile (*args, **kwargs):
        start_time = time.time()
        ret = fn(*args, **kwargs)
        elapsed = time.time() - start_time
        print "Function %s finished in %.3f"%(fn.__name__, elapsed)
        return ret
    return with_profile
    
@profile
def solve_queens(N):
    N = int(sys.argv[1])#int(raw_input(''))
    b = []
    for i in range (N):
        b.append([])
        for j in range (N):
            b[i].append(0)
    global primes
    primes = get_primes(N)
    if(insert(0,N,b)):
        return b
    else:
        return None


import sys
from prime_sieve import get_primes
if __name__ == "__main__":
    N = int(sys.argv[1])#int(raw_input(''))
    global space
    space = range(N)
    b = solve_queens(N)
    if b is not None:
        print_result(b)
        #print_verbose(b)
