#!/bin/python
# Head ends here
def nextMove(n,x,y, grid):
#print all the moves here
    x_moves = {1:'RIGHT',-1:'LEFT'}
    y_moves = {1:'DOWN', -1:'UP'}
    #looking for princess
    for i in range(0,m):
        for j in range(0,m):
            if grid[i][j] == 'p':
                px , py = j, i
                dx = px - x 
                dy = py - y             
                #print ((x_moves[dx/abs(dx)] + '\n') * abs(dx))[:-1]
                #print ((y_moves[dy/abs(dy)] + '\n') * abs(dy))[:-1]
                if dx != 0 : 
                    return x_moves[dx/abs(dx)]
                elif dy != 0:
                    return y_moves[dy/abs(dy)]
    return ""
                        
# Tail starts here
m = input()
x, y = [int(i) for i in raw_input().strip().split()]
grid = []

for i in xrange(0, m):
    grid.append(raw_input().strip())
#print grid
print nextMove(m, y, x, grid)
