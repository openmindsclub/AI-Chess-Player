# main file
from Board import *


def NegaMax(board, d, j=None):  # d for depth
    # if j:
    #     board.push(j)
    if d == 0:
        return evaluate(board)

    for i in range(d):
        return max({board.push(j)(j, (-1**i) * NegaMax(board, d-1, j))
                    for j in moveTree(board)}, key=lambda x: x[1])


def moveTree(board):
    return list(board.legal_moves)


board = chess.Board()

NegaMax(board, 3)
