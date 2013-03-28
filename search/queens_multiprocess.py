"""
Queens have always hated each other. Traditionally when queens were placed on a chessboard a queen gets jealous of another if:

They are both in the same row.
They are both in the same column.
They can see each other diagonally i.e lie in a line inclined 45 degrees or 135 degrees to the base of board.
But now the hatred has increased and the new condition is that no three of them should lie in any straight line (this line need not be aligned 45 degrees or 135 degrees to the base of chess board).
"""
result = [] # this serves mainly as an index to avoid iteration
from multiprocessing import Pool

def cross_line_worker(x,y,points, N):
    drop = set()
    #drop = []
    for b, a in enumerate(points[(y+1):]):
        x2 = a
        y2 = b + y + 1
        dx = x2 - x
        dy = y2 - y
        n = (len(points) - y ) * dx/float(dy)
        if n - int(n) == 0 and x + n >= 0 and x + n < N:
            drop.add(x + int(n))
            #drop.append(x + int(n))
    return drop

pool = Pool(processes=4)
#space = None
cache = dict()



def cross_lines(r,N,drop):
    collect = []
    avoid = []
    for y, x in enumerate(result[:-1]):
        task = []
        task.append(x)
        task.append(y)
        task.append(result)
        task.append(N)
        collect.append(pool.apply_async(cross_line_worker, task))

    for res in collect:
        s = res.get()
        #avoid.append(s)
        if s is not None:
            drop = drop | res.get()
    #avoid.append(result)
    

    #avoid = avoid + result
    return drop 
"""        
def cross_line_worker(x,y,points, N):
    drop = set()
    for b, a in enumerate(points[(y+1):]):
        x2 = a
        y2 = b + y + 1
        dx = x2 - x 
        dy = y2 - y 
        n = (r - y ) * dx/float(dy)
        if n - int(n) == 0 and x + n >= 0 and x + n < N:
            drop.add(x + int(n))
"""

def insert(r,N):
    """ insert a queen into row r of board b """ 
    drop = set(result)
    #drop = set()
    drop = cross_lines(r, N, drop)
    #cross out diagonals intersection
    for y, x in enumerate(result):
        c = x + (y -r)
        if c < N and c >=0:
            drop.add(c)
        c = x - (y -r)
        if c >= 0 and c < N: 
            drop.add(c)

    #cross out lines intersections
    #drop = cross_lines(r,N,drop)
    #get possible columns
    for c in (x for x in space if x not in drop):
        result.append(c)
        if r < (N-1):
            if(insert(r + 1, N)):
                return True
            else:
                result.pop()
        else:
            return True
    return False

        
def print_result():
    """ print result """ 
    print ' '.join(str(n + 1) for n in result)
import time
def profile(fn):
    def with_profile (*args, **kwargs):
        start_time = time.time()
        ret = fn(*args, **kwargs)
        elapsed = time.time() - start_time
        print "Function %s finished in %.3f"%(fn.__name__, elapsed)
        return ret
    return with_profile
import sys

@profile
def solve_queens(N):
    if(insert(0,N)):
        print_result()

from prime_sieve import get_primes
if __name__ == "__main__":
    N = int(sys.argv[1])#int(raw_input(''))
    global space
    space = range (N)
    global primes
    primes = get_primes(N)
   
    solve_queens(N)
    #if(insert(0,N)):
    #    print_result()
        #print_verbose(b)
