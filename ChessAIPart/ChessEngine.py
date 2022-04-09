"""
this class is responsible for storing all the current information about chess game and determine the valide move at the current state.
it will also keep a move log
"""

class GameState():
    def __init__(self):
        """the board is 8X8 list ,each element of the list has two characters:
        the first one represents the color of the piece
        the second one represents the name of the piece
        -- represents an empty space"""
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                              "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]
        self.player_one = False
        self.player_two = False
   

    #take a move as parameter and execute it 
    def make_move(self, move):
        self.board [move.start_row][move.start_col] = "--"
        self.board [move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) #log the move so we can undo later
        self.white_to_move = not self.white_to_move #swap players
       
        # update king's location if moved
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
        
        # pawn promotion
        if move.is_pawn_promotion:
            #if a human is playing
            if (self.player_one and self.white_to_move) or (self.player_two and not self.white_to_move):
                promoted_piece = input("Promote to Q, R, B, or N:") 
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
                
            else:
            #if ai is playing
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
        
        # enpassant move
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advance
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        # castle move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # king-side castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                    move.end_col + 1]  # moves the rook to its new square
                self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
            else:  # queen-side castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                    move.end_col - 2]  # moves the rook to its new square
                self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook

        self.enpassant_possible_log.append(self.enpassant_possible)

        #update castling rights-whenever it's a rook or a king move
        self. update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs))


    #undo the last move made
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move #swap players
         
          # update the king's position if needed
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
         
            # undo en passant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"  #remove the pawn that was added
                self.board[move.start_row][move.end_col] = move.piece_captured #put the pawn back on the correct square that was captured from
           
            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]
            #undo castling rights
            self.castle_rights_log.pop() # get rid of the new castle rights from the move we are undoing
            self.current_castling_rights = self.castle_rights_log[-1] # set the current castle rights to the last one in the list
           
            # undo the castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king-side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:  # queen-side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'
            
            self.checkmate = False
            self.stalemate = False

#update the castle rights given the move
    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castling_rights.wqs = False
            self.current_castling_rights.wks = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bqs = False
            self.current_castling_rights.bks = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.bks = False
            
        #if a rok is captured
        if move.piece_captured == "wR":
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_captured == "bR":
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False



    def get_valid_moves(self):
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                          self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()

        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check:
            """if the king is in check, we have some moves that are not valid and we 
               here have two cases, one check or two checks"""
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.get_all_possible_moves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                #else i can move to the enemy piece or any square between the king and attacking piece
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i,
                                        king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list of moves backwards
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:  #the king is not in check , so all moves are valid
            moves = self.get_all_possible_moves()
            if self.white_to_move:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.current_castling_rights = temp_castle_rights

        return moves
    
    #  Determine if a current player is in check
    def in_check(self):
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])


    #Determine if enemy can attack the square row col
    def square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move  #switch to opponent's point of view
        opponents_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  #square is under attack
                return True
        return False
    

    # All moves without considering checks.
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves) #call the appropriate move function based on piece type
        return moves
    

    def check_for_pins_and_checks(self):
        pins = []  #squares pinned and the direction its pinned from
        checks = []  #squares where enemy is applying a check
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        #get the positions of all possible checks 
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = () #reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    #case ally peace
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    #case enemy peace, we need to see what type of enemy peace it's
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) only 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (
                            4 <= j <= 7 and enemy_type == "B") or (        
                             i == 1 and enemy_type == "p" and (
                            (enemy_color == "w" and 6 <= j <= 7) or(enemy_color == "b" and 4 <= j <= 5))) or (
                              enemy_type == "Q") or(
                             i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                #here end_row and end_col will represent the position of the enemy piece(end_piece)
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board

        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks
                    

    #get all pawn moves for the pawn located at row, col and all those moves to the list
    def get_pawn_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move: #white pawn moves
            if self.board[row-1][col] == "--": #1 square pawn advanced
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row-1, col), self.board))
                    if row == 6 and self.board[row-2][col] == "--": #2 squares pawn advanced
                        moves.append(Move((row, col),(row-2, col), self.board))
            if col-1 >=0: #captures to the left
                if self.board[row-1][col-1][0] == 'b':
                     if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, col),(row-1, col-1),self.board))
                elif (row - 1 ,col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row-1, col-1), self.board, is_enpassant_move=True))
            if col+1<=7: #captures to the right
                if self.board[row-1][col+1][0] == 'b':
                     if not piece_pinned or pin_direction == (-1, 1 ):
                         moves.append(Move((row, col),(row-1, col+1), self.board))
                elif (row - 1 ,col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row-1, col+1), self.board, is_enpassant_move=True))
        else: #black pawn moves
            if self.board[row+1][col] == "--": #1 square pawn advanced
                 if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col),(row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] =="--": #2 squares pawn advanced
                        moves.append(Move((row, col),(row+2, col), self.board))
            if col-1 >=0:#captures to the left
                if self.board[row+1][col-1][0] == 'w':
                     if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, col),(row+1, col-1),self.board))
                elif (row + 1 ,col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row+1, col-1), self.board, is_enpassant_move=True))
            if col+1 <= 7: #captures to the right
                if self.board[row+1][col+1][0] == 'w':
                     if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((row, col),(row+1, col+1), self.board))
                elif (row + 1 ,col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row+1, col+1), self.board, is_enpassant_move=True))


    #get all rook moves for the rook located at row, col and all those moves to the list
    def get_rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                """can't remove queen from pin on rook moves, only remove it on bishop moves, 
                    and we need to treat cuz queen moves generate both rook and bishop moves"""
                if self.board[row][col][1] != "Q": 
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, right, right
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col <8: #on board
                   if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                     end_piece = self.board[end_row][end_col]
                     if end_piece == "--": #empty space valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                     elif end_piece[0] == enemy_color: #enemy piece valid
                         moves.append(Move((row, col), (end_row, end_col), self.board))
                         break
                     else: #friendly piece valid
                        break
                else: #out of the board
                    break

    #get all rook moves for the knight located at row, col and all those moves to the list
    def get_knight_moves(self, row, col, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

                      # up/left up/right right/up right/down down/left down/right left/up left/down

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))


    #get all rook moves for the bishop located at row, col and all those moves to the list
    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))#4 diagonals
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8): #bishop can move max of 7 squares
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col <8: #on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                     end_piece = self.board[end_row][end_col]
                     if end_piece == "--": #empty space valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                     elif end_piece[0] == enemy_color: #enemy piece valid
                         moves.append(Move((row, col), (end_row, end_col), self.board))
                         break
                     else: #friendly piece valid
                        break
                else: #out of the board
                    break


    #get all rook moves for the queen located at row, col and all those moves to the list
    def get_queen_moves(self, row, col, moves): 
        #a queen can move as rook + bishop
        self.get_rook_moves(row, col,moves)
        self.get_bishop_moves(row, col, moves)


    #get all rook moves for the king located at row, col and all those moves to the list
    def get_king_moves(self, row, col, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),(1, 1))
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)
            
            self.get_castle_moves


#generate all valid castle moves for the king at (row, col) and add them to the list of moves.
    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return  # can't castle while in check
        if (self.white_to_move and self.current_castling_rights.wks) or \
                (not self.white_to_move and self.current_castling_rights.bks):
            self. get_king_side_castleMoves(row, col, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or \
                (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queen_side_castleMoves(row, col, moves)

    def get_king_side_castleMoves(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))

    def get_queen_side_castleMoves(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    #maps keys to values
    #key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, pawn_promotion = False, is_enpassant_move = False, is_castle_move = False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (self.piece_moved == "bp" and self.end_row == 7)
        # en passant
        self.is_enpassant_move =  is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        #castle move
        self.is_castle_move = is_castle_move

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col


    def __eq__(self, other):
        """
        overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        #you can add to make this as real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.ranks_to_ranks[row]