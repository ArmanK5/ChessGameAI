"""
This is the main driver file. It will be responsible for handling user input and displaying the current GameState object
"""

import pygame as pygame_module

import ChessAI
import ChessEngine

pygame_module.init()
square_width = square_height = 512
dim = 8  # dimensions of a chessboard are 8x8
square_size = square_height / dim
IMAGES = {}  # images pieces


'''
Creating an array of images that have the corresponding name of the piece and will be called once in main
'''


def create_pieces_images():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = pygame_module.transform.scale(pygame_module.image.load("images/" + piece + ".png"),
                                                      (square_size, square_size))



'''
The main driver for our code. This will handle user input and updating the graphics
'''


def main():
    pygame_module.init()
    screen = pygame_module.display.set_mode((square_width, square_height))
    screen.fill(pygame_module.Color("white"))
    game_state = ChessEngine.game_state()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # move made bool
    create_pieces_images()  # only do this once
    running = True
    end_game = False  # for when stalemate or checkmate has occurred
    current_square_selected = ()  # no square is selected initially, keep track of the last click of the user (tuple: (row,col))
    mouse_clicks = []  # keep track of player clicks (two tuples: [(6,4), (4,4)]
    player_white = True  # Human = True, AI = False
    player_black = False
    while running:
        if game_state.white_turn and player_white:  # check if current player is an ai or a real person using 'and' logic
            is_human_turn = True
        elif not game_state.white_turn and player_black:
            is_human_turn = True
        else:
            is_human_turn = False
        for e in pygame_module.event.get():
            if e.type == pygame_module.QUIT:
                running = False
            elif e.type == pygame_module.KEYDOWN:
                if e.key == pygame_module.K_z:  # undo when 'z' is pressed
                    game_state.undo_move()
                    valid_moves = game_state.get_valid_moves()
                if e.key == pygame_module.K_r:  # reset when 'r' is pressed
                    game_state = ChessEngine.game_state()
                    valid_moves = game_state.get_valid_moves()
                    move_made = False
                    current_square_selected = ()
                    mouse_clicks = []
            elif e.type == pygame_module.MOUSEBUTTONDOWN:
                if not end_game and is_human_turn:
                    location = pygame_module.mouse.get_pos()  # (x, y) location of mouse
                    file = location[0] // square_size
                    row = location[1] // square_size
                    if current_square_selected == (row, file):  # the user clicked the same square twice
                        current_square_selected = ()  # deselect
                        mouse_clicks = []  # clear player clicks
                    else:
                        current_square_selected = (row, file)
                        mouse_clicks.append(current_square_selected)  # append for both 1st and 2nd clicks
                    if len(mouse_clicks) == 2:  # after 2nd click
                        move = ChessEngine.move(mouse_clicks[0], mouse_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])  # valid moves is instead of using player generated move to engine generated move
                                move_made = True
                                current_square_selected = ()  # reset user clicks
                                mouse_clicks = []
                        if not move_made:  # preventative for bugs
                            mouse_clicks = [current_square_selected]


        #AI move finder
        if not end_game and not is_human_turn:
            ai_move = ChessAI.min_max(game_state,valid_moves)
            game_state.make_move(ai_move)
            move_made = True


        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        create_game_state(screen, game_state, valid_moves, current_square_selected)

        if game_state.stale_mate:
            end_game = True
            create_text(screen, "Stalemate")
        elif game_state.check_mate:
            end_game = True
            if game_state.white_turn:
                create_text(screen, "Black wins by checkmate")
            else:
                create_text(screen, "White wins by checkmate")


        pygame_module.display.flip()


'''
Square highlight for piece movement
'''

def square_highlight(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        row, file = sq_selected
        row = int(row)
        file = int(file)
        if gs.board[row][file][0] == (
                'w' if gs.white_turn else 'b'):  # if the piece can actually be moved
            # highlight the selected square
                surface_square = pygame_module.Surface((square_size, square_size))
                surface_square.set_alpha(200)  # value for transparent
                surface_square.fill(pygame_module.Color('navy'))
                screen.blit(surface_square, (file * square_size, row * square_size))
                surface_square.fill(pygame_module.Color('purple'))
                for move in valid_moves:  # highlight the moves selected piece can take
                    if move.initial_row == row and move.first_file == file:  # checking the piece is the same one in valid moves
                        screen.blit(surface_square, (square_size * move.last_file, square_size * move.last_row))



'''
Responsible for all the graphics within a current game state
'''


def create_game_state(screen, gs, valid_moves, sq_selected):  # each function is essentially a layer where
    # if I put pieces before highlighting the highlighting will overlap the piece aswell
    create_board(screen)  # draw the squares on the board
    square_highlight(screen, gs, valid_moves, sq_selected)  # highlight piece when selected
    create_pieces(screen, gs.board)  # draw pieces on top of those squares


'''
Draw the squares on the board. The top left square is always light.
'''


def create_board(screen):
    colors = [pygame_module.Color("white"), pygame_module.Color(0, 180, 216)]
    for r in range(dim):
        for c in range(dim):
            color = colors[((r+c)%2)] # because how chessboard work the coords added together if its odd its dark square if its even its light
            pygame_module.draw.rect(screen, color, pygame_module.Rect(c * square_size, r * square_size, square_size, square_size))

'''
Draw the pieces on the board using the current game_state.board
'''


def create_pieces(screen, board):
    for row in range(dim):
        for file in range(dim):
            piece = board[row][file]
            if piece != "E":  # not empty square
                screen.blit(IMAGES[piece], pygame_module.Rect(file * square_size, row * square_size, square_size, square_size))


def create_text(screen, text):  # create text function
    font = pygame_module.font.SysFont("Ariel", 40, True, False)
    text_obj = font.render(text, 0, pygame_module.Color("Red"))
    text_loc = pygame_module.Rect(0, 0, square_width, square_height).move(square_width / 2 - text_obj.get_width() / 2,
                                                                          square_height / 2 - text_obj.get_height() / 2)  # centering text on screen
    screen.blit(text_obj,text_loc)


main()