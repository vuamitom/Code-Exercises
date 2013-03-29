"""
Queens have always hated each other. Traditionally when queens were placed on a chessboard a queen gets jealous of another if:

They are both in the same row.
They are both in the same column.
They can see each other diagonally i.e lie in a line inclined 45 degrees or 135 degrees to the base of board.
But now the hatred has increased and the new condition is that no three of them should lie in any straight line (this line need not be aligned 45 degrees or 135 degrees to the base of chess board).
"""
result = [] # this serves mainly as an index to avoid iteration

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

cache = dict()

def queen_worker(task_queue, result_queue):
    while(True):
        try:
            task = task_queue.pop()
            if task is not None:
                #do smth
                drop = cross_line_worker(task[0],task[1],task[2],task[3])
                result_queue.append(drop)
        except IndexError:
            pass
            #do nothing



def cross_lines(r,N,drop):
    for y, x in enumerate(result[:-1]):
        task_list.append((x, y, result, N))

    while(len(task_list) > 0):
        for s in result_list:
            if s is not None:
                drop = drop | s
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


from multiprocessing import Process,Manager 
if __name__ == "__main__":
    N = int(sys.argv[1])#int(raw_input(''))
    global space
    space = range (N)
    manager = Manager()
    global task_list
    task_list = manager.list()
    result_list = manager.list()
    workers = []
    for i in range(4):
        p = Process(target = queen_worker, args = (task_list, result_list))
        p.start()
    solve_queens(N)
    for p in workers:
        p.join()

