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
    "p": -1,
    "n": -3,
    "b": -3,
    "r": -5,
    "q": -9,

}


def Mevaluate(board):
    "evaluate the current position of the board purely based on material advantage"
    eval = 0
    for i in board.fen():
        eval += piece_value.get(i)
    return eval


def evaluate(board):
    return Mevaluate(board)


if __name__ == "__main__":
    # create board object
    board = chess.Board()

    # display chess board
    print(board)

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
