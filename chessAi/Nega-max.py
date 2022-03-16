# main file
from Board import *
from Classes import *


def NegaMax(board, d, movebranche=Movebranche()):  # d for depth
    # if j:
    #     board.push(j)
    if d == 0:
        movebranche.branche_value(evaluate(board))
        return movebranche

    for i in range(d):
        evalList = []
        for j in moveTree(board):
            board.push(j)
            movebranche.addmove(j)
            #  * NegaMax(board, d-1)
            evalList.append(NegaMax(board, d-1, movebranche))
            board.pop()  # returns the board to the state before the move j (the last move)
            movebranche.pop()  # "" the move branche ""   ""   ""   ""  ""
        return max(evalList, key=lambda x: (-1**i) * x.value)


def moveTree(board):
    return list(board.legal_moves)


board = chess.Board()

print(NegaMax(board, 5).moves)
