# IDEAS:
# Backtracking
# Prefilter 
# Post-backtrack filter (?)

# Board setup: 0-4 = # cells, 5 = wall, 6 = nothing, 7 = light, 8 = cell covered by light, 9 = definitely not here!, 

import copy
import time

def printBoard(board):
    print("\033[2J")
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
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
        x, y = i + dx, j + dy
        if 0 <= x < X_LEN and 0 <= y < Y_LEN:
            if board[x][y] == 6:
                changes[(x, y)] = 6
                board[x][y] = 9

    return changes

def getValidSquares(board):  # IDEA: different sort? if we can find a better (partial) order we should be happy
    def goodNeighbor(x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < X_LEN and 0 <= ny < Y_LEN:
                if 1 <= board[nx][ny] <= 4:
                    return True
        return False

    positions = [
        (x, y)
        for x in range(X_LEN)
        for y in range(Y_LEN)
        if board[x][y] == 6
    ]

    return sorted(positions, key=lambda pos: not goodNeighbor(*pos))

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

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = i0 + dx, j0 + dy
        if 0 <= x < X_LEN and 0 <= y < Y_LEN and board[x][y] < 5:
            changes[(x, y)] = board[x][y]
            board[x][y] -= 1
            if board[x][y] == 0:
                changes |= fillXs(board, x, y)

    return changes

def impossibleCheck(board):
    for x in range(X_LEN):
        for y in range(Y_LEN):
            if 1 <= board[x][y] <= 4:
                count = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    xC, yC = x + dx, y + dy
                    if 0 <= xC < X_LEN and 0 <= yC < Y_LEN and board[xC][yC] == 6:
                        count += 1
                if count < board[x][y]:
                    return True

    return False

TEMP_K = 0

def track(board):
    # global TEMP_K
    # TEMP_K += 1
    # if TEMP_K >= 100000:
    #     quit()

    # printBoard(board)
    # print()
    # input()
    
    # for each valid square in the obvious ordering:
    # fill it
    # call track
    # if no valid square, undo what we've just done and be sad (lasiest way to do this is deepcopy, so that's exactly what we'll do)

    # check we haven't already made it impossible

    impossible = impossibleCheck(board)
    if impossible:
        return False

    xChanges = {}

    for square in getValidSquares(board):
        changes = fillValidSquare(board, square)
        out = track(board)
        if out != False:
            return out
        else:
            for (pos, prevVal) in changes.items():
                board[pos[0]][pos[1]] = prevVal

        xChanges[square] = 6
        board[square[0]][square[1]] = 9

    for (pos, prevVal) in xChanges.items():
        board[pos[0]][pos[1]] = prevVal

    # check if we're done!
    for i in range(X_LEN):
        for j in range(Y_LEN):
            if board[i][j] == 6 or board[i][j] == 9 or 1 <= board[i][j] <= 4:
                return False

    return board


X_LEN = 0
Y_LEN = 0

def solve(board):
    global X_LEN, Y_LEN
    X_LEN = len(board)
    Y_LEN = len(board[0])

    printBoard(board)
    print("-----")
    
    initialXFill(board)
    # printBoard(board)
    # quit()

    board = track(board)

    printBoard(board)

def main():
    board = []
    for _ in range(10):
        board.append([6] * 10)

    # for zero in [(0,1),(0,3),(0,6),(0,7),(2,8),(3,0),(3,3),(3,7),(4,6),(5,1),(6,3),(6,8),(7,5),(8,1),(8,7)]:  # (x,y)
    #     board[zero[1]][zero[0]] = 0  # (y,x)

    solve([[5, 5, 1, 6, 6, 6, 5, 6, 6, 6], [5, 6, 6, 6, 2, 6, 6, 6, 6, 6], [6, 6, 6, 6, 5, 6, 6, 0, 6, 6], [6, 2, 6, 6, 6, 6, 6, 6, 6, 0], [6, 6, 6, 6, 5, 6, 6, 6, 6, 6], [0, 6, 0, 6, 0, 5, 6, 5, 2, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [5, 6, 1, 6, 5, 6, 6, 6, 6, 5], [6, 6, 6, 6, 6, 6, 3, 6, 6, 5], [6, 6, 5, 6, 2, 6, 6, 6, 5, 5]])

if __name__ == "__main__":
    main()