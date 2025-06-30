# IDEAS:
# Backtracking
# Prefilter 
# Post-backtrack filter (?)

# Board setup: 0-4 = # cells, 5 = wall, 6 = nothing, 7 = light, 8 = cell covered by light,

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
        print()

def incrementPos(maxX, maxY, pos):  # funky
    if pos == (maxX, maxY):
        return None
    if pos[1] == maxY:
        return (pos[0] + 1, 0)
    else:
        return (pos[0], pos[1] + 1)

# def getNextValidSquare(board, pos):
#     while (pos := incrementPos(len(board) - 1, len(board[0]) - 1, pos)) != None:
#         # check if pos is valid
#         (i, j) = pos
#         if board[i][j] != 6: continue
#         if i-1 >= 0 and board[i-1][j] == 0: continue
#         if i+1 < len(board) and board[i+1][j] == 0: continue
#         if j-1 >= 0 and board[i][j-1] == 0: continue
#         if j+1 < len(board[0]) and board[i][j+1] == 0: continue

#         return pos

#     return None

def getValidSquares(board):
    pos = (0, -1)  # getNextValidSquare assumes "current" square is already included, so start off the board so (0,0) isn't missed
    positions = []
    # while (pos := getNextValidSquare(board, pos)) != None:
    #     positions.append(pos)

    while (pos := incrementPos(len(board) - 1, len(board[0]) - 1, pos)) != None:
        # check if pos is valid
        (i, j) = pos
        if board[i][j] != 6: continue
        if i-1 >= 0 and board[i-1][j] == 0: continue
        if i+1 < len(board) and board[i+1][j] == 0: continue
        if j-1 >= 0 and board[i][j-1] == 0: continue
        if j+1 < len(board[0]) and board[i][j+1] == 0: continue

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
    while (i < len(board) and board[i][j0] > 5):
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
    while (j < len(board[0]) and board[i0][j] > 5):
        if board[i0][j] != 7:
            changes[(i0, j)] = board[i0][j]
            board[i0][j] = 8
        j += 1

    if i0 - 1 >= 0 and board[i0-1][j0] < 5: 
        changes[(i0-1, j0)] = board[i0-1][j0]
        board[i0-1][j0] -= 1
    if i0 + 1 < len(board) and board[i0+1][j0] < 5: 
        changes[(i0+1, j0)] = board[i0+1][j0]
        board[i0+1][j0] -= 1
    if j0 - 1 >= 0 and board[i0][j0-1] < 5: 
        changes[(i0, j0-1)] = board[i0][j0-1]
        board[i0][j0-1] -= 1
    if j0 + 1 < len(board[0]) and board[i0][j0+1] < 5: 
        changes[(i0, j0+1)] = board[i0][j0+1]
        board[i0][j0+1] -= 1

    return changes

TEMP_K = 0

def track(board):
    global TEMP_K
    TEMP_K += 1
    if TEMP_K >= 5000:
        quit()

    # printBoard(board)
    # print()
    # time.sleep(1)
    
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
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 6:
                return False

    return board



def main():
    board = []
    for _ in range(10):
        board.append([6] * 10)

    for zero in [(0,1),(0,3),(0,6),(0,7),(2,8),(3,0),(3,3),(3,7),(4,6),(5,1),(6,3),(6,8),(7,5),(8,1),(8,7)]:  # (x,y)
        board[zero[1]][zero[0]] = 0  # (y,x)

    test = track(board)

    printBoard(test)

if __name__ == "__main__":
    main()