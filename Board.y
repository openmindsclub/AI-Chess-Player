import chess

if __name__ == "__main__":
    # create board object
    board = chess.Board()

    # display chess board
    print(board)

    print(board.legal_moves)  # legal moves

    # moving players
    board.push_san("e4")
    # It means moving the particular piece at
    # e place to 4th position

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
