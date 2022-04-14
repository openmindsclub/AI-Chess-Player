import chess

"""
Basic evaluation function , going to count the material on each side and then evaluate the position 

at a certain depth (number of moves in the future)

TO NOTE:
    any sequance of checks, taking pieces will NOT be concidered the end of the calulations to ensure better evaluation of the position 
    
    this will be added to the nega max function later inchallah
"""
piece_value = {
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 90,
    "p": -1,
    "n": -3,
    "b": -3,
    "r": -5,
    "q": -9,
    "k": -90

}


def readable_FEN(board):
    FEN = [list(_) for _ in board.fen().split()[0].split("/")]
    readable_fen = []
    for rank in FEN:
        t_rank = []

        for i in rank:
            if i.isdigit():
                {t_rank.append("0") for j in range(int(i))}
            else:
                t_rank.append(i)
        readable_fen.append(t_rank.copy())
    return readable_fen


def Mevaluate(board):
    "evaluate the current position of the board purely based on material advantage"
    eval = 0
    for i in board.fen().split()[0]:
        if i in piece_value.keys():
            eval += piece_value.get(i)
    return eval


def Pevaluate(board):
    "evaluates the position based on positional advantage"
    eval = 0
    FEN = readable_FEN(board)

    for rank in [4, 5]:
        for file in [4, 5]:
            if FEN[rank][file] == "p":
                eval -= 0.1
            if FEN[rank][file] == "P":
                eval += 0.1

    for rank, file in zip(range(3, 6), range(2, 7)):
        if not FEN[rank][file].isdigit():
            if FEN[rank][file].lower() == FEN[rank][file]:
                eval -= 0.1
            if FEN[rank][file].upper() == FEN[rank][file]:
                eval += 0.1

    return eval


def moveTree(board):
    return list(board.legal_moves)


def evaluate(board):
    return Mevaluate(board)+Pevaluate(board)


if __name__ == "__main__":
    # create board object
    board = chess.Board()

    # display chess board
    print(board)

    print(board.fen().split()[0])

    print(board.legal_moves)  # legal moves

    print(list(board.legal_moves))  # legal moves

    print(list(board.legal_moves)[0])  # legal moves

    # moving players
    board.push_san("e4")
    # It means moving the particular piece at
    # e place to 4th position
    'h7h5'

    # Display chess board again to see changes
    print(board)

    # Verifying check mate
    print("THIS IS THE CHECKMATE VALUE")
    print(board.is_checkmate())
    # helps to see if the game is a win or a draw
    # Verifying stalemate
    print(board.is_stalemate())

    # code
    print(board.is_check())

    """
    this module happens to have a lot more functionalities so i encourage you to play with it more 
    
    i only wrote what i thought was good for our progress
    this file will eventually hold an evalutaion function of 
    the position inchallah
    
    """
    print("this part highlights the behavior of the material evaluation function")
    print(Mevaluate(board))
    board.push_san("d5")
    board.push_san("exd5")
    print(Mevaluate(board))
    board.push_san("Qxd5")
    print(Mevaluate(board))
    board.push_san("d4")
    board.push_san("Qxd4")
    print(Mevaluate(board))
    board.push_san("Qxd4")
    print(Mevaluate(board))

    print(board.fen().split())
    print(readable_FEN(board))
    print("______________________________________________________________")

    print(Pevaluate(board))
