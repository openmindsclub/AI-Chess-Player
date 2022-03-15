# main file
from Board import *
from Classes import *


def NegaMax(board, d, j=None):  # d for depth
    # if j:
    #     board.push(j)
    if d == 0:
        return evaluate(board)

    for i in range(d):
        for j in moveTree(board):
            board.push(j)
            Meval = {}
            Meval[j] = (-1**i) * NegaMax(board, d-1, j)
        return max(Meval, key=lambda x: x[1])


def moveTree(board):
    return list(board.legal_moves)


board = chess.Board()

NegaMax(board, 3)
