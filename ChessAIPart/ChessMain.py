"""
this is our main driver file. 
"""

import pygame as p
import ChessEngine
import ChessAi

WIDTH = 512
HEIGHT = 512
DIMENSIONS = 8 #dimensions of chess board are 8X8
BOARD_WIDTH = BOARD_HEIGHT = 512
SQ_SIZE = HEIGHT // DIMENSIONS 
IMAGES = {}

#load images
def load_images():
    pieces = ["bp", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
              "wp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images\\"+piece +".png"), (SQ_SIZE, SQ_SIZE))

#the main driver of our code, this will handle user input and updating the graphics
def main():
    p.init()
    screen = p.display.set_mode((HEIGHT, WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valide_moves = game_state.get_valid_moves() #for each move we check if it's valide first
    move_made = False #flag variable for when a move is made ,to change the list pf valide moves

    load_images()
    running = True
    sq_selected = () #no of the selected square, keep track of the last click of the user(tuple: (row, col)) 
    player_clicks = [] #keep track of player clicks (two tuples : [(current square), (next square)])
    game_over = False
    game_state.player_one = True #if a human is playing white, then this will be true , else if an ai is playing then false
    game_state.player_two = False #same for black

    
    while running:
        human_turn = (game_state.white_to_move and game_state.player_one) or \
        (not game_state.white_to_move and game_state.player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler 
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn :
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    #treat different cases of clicks 
                    if sq_selected == (row, col): #click on the same current square
                        sq_selected = () #deselect
                        player_clicks = [] #clear player clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected) #append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn: #it's the second click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1],  game_state.board) 
                        for i in range(len(valide_moves)):
                            if move == valide_moves[i]:
                                game_state.make_move(valide_moves[i])
                                move_made = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                               player_clicks = [sq_selected] #delete the wrong second move    

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    game_state.undo_move()
                    move_made = True
                    game_over = False

                if e.key == p.K_r:  # reset the game when r is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False
            
            #Ai move finder
            if not game_over and not human_turn:
                ai_move = ChessAi.find_best_move(game_state, valide_moves)
                if ai_move is None:
                    ai_move = ChessAi.find_random_move(valide_moves)
                
                game_state.make_move(ai_move)
                move_made = True

            if move_made:
                valide_moves = game_state.get_valid_moves() #set new list of valid moves
                move_made = False
            
            draw_game_state(screen, game_state)

            if game_state.checkmate:
                    game_over = True
                    if game_state.white_to_move:
                        drawEndGameText(screen, "Black wins by checkmate")
                    else:
                        drawEndGameText(screen, "White wins by checkmate")
            elif game_state.stalemate:
                game_over = True
                drawEndGameText(screen, "Stalemate")

        p.display.flip()

#responsible for all graphics within  a current state game
def  draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

#draw the squares on the board
def draw_board(screen):
    global colors
    colors = [p.Color("White"), p.Color("gray")]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[((row+col) %2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#draw the pieces on the board using the current GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSIONS):
        for col in range (DIMENSIONS):
            piece = board[row][col]
            if piece != "--": #if it's not an empty square
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#draw a text on the board at the end of the game
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()






