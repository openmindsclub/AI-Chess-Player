# main file
from copy import deepcopy
from Board import *
from Classes import *


def NegaMax(board, d, alpha=-1000, beta=1000, movebranche=Movebranche()):  # d for depth
    # if j:
    #     board.push(j)
    if d == 0:
        movebranche.branche_value(evaluate(board))
        return movebranche
    if board.is_checkmate():
        movebranche.branche_value(
            1000 if board.fen().split()[1] == 'b' else -1000)
        return movebranche
    if board.is_stalemate():
        movebranche.branche_value(0)
        return movebranche

    i = -1 if board.fen().split()[1] == 'b' else 1
    chosen_branche = Movebranche()
    chosen_branche.branche_value(-i*10000)
    for j in moveTree(board):
        board.push(j)
        movebranche.addmove(j)
        #  * NegaMax(board, d-1)
        branche = NegaMax(board, d-1, alpha, beta, deepcopy(movebranche))
        chosen_branche = max(chosen_branche, branche,
                             key=lambda x: i * x.value)

        board.pop()  # returns the board to the state before the move j (the last move)
        movebranche.pop()  # "" the move branche ""   ""   ""   ""  ""
        if i == 1:
            alpha = max(alpha, branche.value)
            if beta <= alpha:
                break
        if i == -1:
            beta = min(beta, branche.value)
            if beta <= alpha:
                break

    return chosen_branche


board = chess.Board()
board.push_san('f3')
board.push_san('e5')
board.push_san("e3")
board.push_san("d5")
board.push_san("Bb5")
board.push_san("Nc6")
board.push_san("Ke2")
board.push_san("Bc5")
board.push_san("Kf1")
board.push_san("Nf6")
board.push_san("Ne2")
board.push_san("O-O")

print(board)
best_moves = NegaMax(board, 5).moves
print(best_moves)
