from copy import deepcopy
from Board import *
from Classes import *


def Positions(board, d, positions):
    if d == 0:
        positions.append(board)
        return positions
    for j in moveTree(board):
        Positions(deepcopy(board.push(j)), d-1, positions)
        board.pop()
    return positions


def NegaMax2(board, d):
    pass
