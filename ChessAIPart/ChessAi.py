import random
from shutil import move
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
def find_random_move(valide_moves):
    return valide_moves[random.randint(0, len(valide_moves)-1)]

#find the best move 
def find_best_move_greedy(game_state, valide_moves):
    turn_multiplier = 1 if game_state.white_to_move else -1
    max_score = -CHECKMATE
    best_move = None
    for player_move in valide_moves:
        game_state.make_move(player_move)
        if game_state.checkmate:
            score = CHECKMATE
        elif game_state.stale_mate:
            score = STALEMATE
        else:
            score = turn_multiplier * score_board(game_state)

        if score > max_score:
            max_score = score
            best_move = player_move

        game_state.undo_move()

def find_best_move(game_state, valide_moves):
    global next_move
    next_move = None
    random.shuffle(valide_moves)
    find_move_nega_max(game_state, valide_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.white_to_move else -1)
    return next_move

def find_move_nega_max(game_state, valide_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)
    max_score = -CHECKMATE
    for move in valide_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

#score the board ,a positive score is good for white, a negative score is good for black.
def score_board(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif game_state.stalemate:
        return STALEMATE

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score