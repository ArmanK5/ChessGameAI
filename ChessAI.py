import random

def random_ai(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

"""
Greedy algorithm
"""

def greedy_algorithm(game_state, valid_moves):
    if game_state.white_turn:  # because it's a zero-sum game black's side is negative
        whiteorblack = 1
    else:
        whiteorblack = -1

    best_move = None
    score_maximum = -1000  # most minimum value possible which is getting checkmated
    for player_move in valid_moves:  # runs through each possible move
        game_state.make_move(player_move)  # makes the move and sees the board score
        if game_state.check_mate:
            score = 1000
        elif game_state.stale_mate:
            score = 0
        else:
            score = whiteorblack * board_score(game_state.board)  # makes it so from either black or white perspective it is trying to get a maximum score
        if score > score_maximum:  # black is trying to get the lowest value of max score as it is zero-sum game
            score_maximum = score
            best_move = player_move
        game_state.undo_move()
    return best_move



def min_max(game_state, valid_moves):
    if game_state.white_turn:  # because it's a zero-sum game black's side is negative
        whiteorblack = 1
    else:
        whiteorblack = -1
    random.shuffle(valid_moves)
    player_best_move = None
    enemy_min_max_score = 1000
    for player_move in valid_moves:  # looks at possible moves from players perspective
        game_state.make_move(player_move)
        enemy_moves = game_state.get_valid_moves()# 1000 represents checkmate
        enemy_max_score = -1000
        for enemy_move in enemy_moves:  # looks at each possible enemy move from every player's move
            game_state.make_move(enemy_move)
            if game_state.check_mate:
                score = -1 * whiteorblack * 1000  # double negative = positive as it flips after looking at opponents next move
            elif game_state.stale_mate:  # 0 represents stalemate
                score = 0
            else:
                score = -1 * whiteorblack * board_score(game_state.board) # makes it so from either black or white perspective it is trying to get a maximum score
            if score > enemy_max_score:  # black is trying to get the lowest value of max score as it is zero-sum game
                enemy_max_score = score
            game_state.undo_move()
        if enemy_min_max_score > enemy_max_score:  # opponents max score is lower then opponents previous score then that is preferable
            enemy_min_max_score = enemy_max_score
            player_best_move = player_move
        game_state.undo_move()
    return player_best_move

"""
Sum of material strength on board
"""

def board_score(board):
    score = 0
    for r in board:  # for each row
        for s in r:  # for each square to get material
            if s[0] == 'w':  # + and - because of zero-sum game
                multiplier = 1
            elif s[0] == 'b':
                multiplier = -1
            else:  # if empty square then next if
                continue
            if s[1] == 'p':
                score += multiplier*1
            elif s[1] == 'N' or s[1] == 'B':
                score += multiplier*3
            elif s[1] == 'r':
                score += multiplier*5
            elif s[1] == 'Q':
                score += multiplier*10
            elif s[1] == 'K':
                score += 0

    return score