# IDEAS:
# Backtracking
# Prefilter 
# Post-backtrack filter (?)

# Board setup: 0-4 = # cells, 5 = wall, 6 = nothing, 7 = light, 8 = cell covered by light, 9 = definitely not here!, 

import copy
import time

def printBoard(board):
    for row in board:
        for item in row:
            if item <= 4:
                print(str(item), end='')
            elif item == 5:
                print("w", end='')
            elif item == 6:
                print(" ", end='')
            elif item == 7:
                print("▫", end='')
            elif item == 8:
                print("█", end='')
            elif item == 9:
                print("x", end='')
        print()

def initialXFill(board):
    for i in range(X_LEN):
        for j in range(Y_LEN):
            if board[i][j] != 6: continue
            if i-1 >= 0 and board[i-1][j] == 0: board[i][j] = 9
            elif i+1 < X_LEN and board[i+1][j] == 0: board[i][j] = 9
            elif j-1 >= 0 and board[i][j-1] == 0: board[i][j] = 9
            elif j+1 < Y_LEN and board[i][j+1] == 0: board[i][j] = 9

def fillXs(board, i, j):
    changes = {}
    if i-1 >= 0 and board[i-1][j] == 6: 
        changes[(i-1,j)] = 6
        board[i-1][j] = 9
    elif i+1 < X_LEN and board[i+1][j] == 0:
        changes[(i+1,j)] = 6
        board[i+1][j] = 9
    elif j-1 >= 0 and board[i][j-1] == 0: 
        changes[(i,j-1)] = 6
        board[i][j-1] = 9
    elif j+1 < Y_LEN and board[i][j+1] == 0: 
        changes[(i,j+1)] = 6
        board[i][j+1] = 9

    return changes

def incrementPos(pos):  # funky
    if pos == (X_LEN - 1, Y_LEN - 1):
        return None
    if pos[1] == Y_LEN - 1:
        return (pos[0] + 1, 0)
    else:
        return (pos[0], pos[1] + 1)

def getValidSquares(board):
    pos = (0, -1)  # getNextValidSquare assumes "current" square is already included, so start off the board so (0,0) isn't missed
    positions = []

    while (pos := incrementPos(pos)) != None:
        # check if pos is valid
        if board[pos[0]][pos[1]] == 6: 
            positions.append(pos)
    
    return positions

def fillValidSquare(board, pos):
    (i0, j0) = pos
    changes = {}
    changes[(i0, j0)] = board[i0][j0]
    board[i0][j0] = 7
    i = i0 - 1
    while (i >= 0 and board[i][j0] > 5):
        if board[i][j0] != 7:
            changes[(i, j0)] = board[i][j0]
            board[i][j0] = 8
        i -= 1
    i = i0 + 1
    while (i < X_LEN and board[i][j0] > 5):
        if board[i][j0] != 7:
            changes[(i, j0)] = board[i][j0]
            board[i][j0] = 8
        i += 1

    j = j0 - 1
    while (j >= 0 and board[i0][j] > 5):
        if board[i0][j] != 7:
            changes[(i0, j)] = board[i0][j]
            board[i0][j] = 8
        j -= 1
    j = j0 + 1
    while (j < Y_LEN and board[i0][j] > 5):
        if board[i0][j] != 7:
            changes[(i0, j)] = board[i0][j]
            board[i0][j] = 8
        j += 1

    if i0 - 1 >= 0 and board[i0-1][j0] < 5: 
        changes[(i0-1, j0)] = board[i0-1][j0]
        board[i0-1][j0] -= 1
        if board[i0-1][j0] == 0:
            changes += fillXs(board, i0-1, j0)
    if i0 + 1 < X_LEN and board[i0+1][j0] < 5: 
        changes[(i0+1, j0)] = board[i0+1][j0]
        board[i0+1][j0] -= 1
        if board[i0+1][j0] == 0:
            changes += fillXs(board, i0+1, j0)
    if j0 - 1 >= 0 and board[i0][j0-1] < 5: 
        changes[(i0, j0-1)] = board[i0][j0-1]
        board[i0][j0-1] -= 1
        if board[i0][j0-1] == 0:
            changes += fillXs(board, i0, j0-1)
    if j0 + 1 < Y_LEN and board[i0][j0+1] < 5: 
        changes[(i0, j0+1)] = board[i0][j0+1]
        board[i0][j0+1] -= 1
        if board[i0][j0+1] == 0:
            changes += fillXs(board, i0, j0+1)

    return changes

TEMP_K = 0

def track(board):
    # global TEMP_K
    # TEMP_K += 1
    # if TEMP_K >= 5000:
    #     quit()

    # printBoard(board)
    # print()
    # time.sleep(2)
    
    # for each valid square in the obvious ordering:
    # fill it
    # call track
    # if no valid square, undo what we've just done and be sad (lasiest way to do this is deepcopy, so that's exactly what we'll do)

    for square in getValidSquares(board):
        changes = fillValidSquare(board, square)
        out = track(board)
        if out != False:
            return out
        else:
            for (pos, prevVal) in changes.items():
                board[pos[0]][pos[1]] = prevVal

    # check if we're done!
    for i in range(X_LEN):
        for j in range(Y_LEN):
            if board[i][j] == 6 or board[i][j] == 9:
                return False

    return board


X_LEN = 0
Y_LEN = 0

def main():
    global X_LEN, Y_LEN
    board = []
    for _ in range(10):
        board.append([6] * 10)

    X_LEN = len(board)
    Y_LEN = len(board[0])

    for zero in [(0,1),(0,3),(0,6),(0,7),(2,8),(3,0),(3,3),(3,7),(4,6),(5,1),(6,3),(6,8),(7,5),(8,1),(8,7)]:  # (x,y)
        board[zero[1]][zero[0]] = 0  # (y,x)

    initialXFill(board)

    board = track(board)

    printBoard(board)

if __name__ == "__main__":
    main()