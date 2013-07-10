#!/usr/bin/python

# Head ends here
def next_move(posx, posy, board):
    if board[posx][posy] == 'd':
        print 'CLEAN'
        return 

    md = 100
    tr, tc = 0 , 0
    for r, c in [(i, j) for i in range(5) for j in range(5)]:
        if board[r][c] == 'd':
            d = abs(posx - r) + abs(posy - c)    
            if d < md:
                md = d
                tr, tc = r, c
    if posy - tc != 0:
        print 'RIGHT' if posy < tc else 'LEFT'
    elif posx - tr != 0:
        print 'DOWN' if posx < tr else 'UP'
    else:
        print ""

# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in raw_input().strip().split()]
    board = [[j for j in raw_input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
