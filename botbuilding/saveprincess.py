#!/bin/python
# Head ends here
def displayPathtoPrincess(n,grid):
#print all the moves here
    cands = [(0,0), (0,m-1),(m-1,0),(m-1,m-1)]
    x_moves = {1:'RIGHT',-1:'LEFT'}
    y_moves = {1:'DOWN', -1:'UP'}

    for c in cands:
        x,y = c
        if grid[y][x] == chr(112):
            #look for bot 
            for i in range(0,m):
                for j in range(0,m):
                    if grid[i][j] == chr(109):
                        dx = x - j 
                        dy = y - i 
                        print ((x_moves[dx/abs(dx)] + '\n') * abs(dx))[:-1]
                        print ((y_moves[dy/abs(dy)] + '\n') * abs(dy))[:-1]
                        break
            break

                        
# Tail starts here
m = input()

grid = []
for i in xrange(0, m):
    grid.append(raw_input().strip())
#print grid
displayPathtoPrincess(m,grid)
