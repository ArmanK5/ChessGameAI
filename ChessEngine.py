"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move Log.
"""

class game_state():
    def __init__(self):
        # the board is a 2d array
        # the first letter of pieces is colour and second is piece type
        # E means empty
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["E", "E", "E", "E", "E", "E", "E", "E"],
            ["E", "E", "E", "E", "E", "E", "E", "E"],
            ["E", "E", "E", "E", "E", "E", "E", "E"],
            ["E", "E", "E", "E", "E", "E", "E", "E"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_log = []
        self.white_turn = True
        self.white_king_location = (7, 4)  # need to keep track of kings location for pins and checks
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()  # coordinates for the square where en passant capture is possible
        self.current_castle_rights = castle_rights(True, True, True, True)
        self.castle_rights_log = [castle_rights(self.current_castle_rights.white_short,
                                                self.current_castle_rights.white_long,
                                                self.current_castle_rights.black_short,
                                                self.current_castle_rights.black_long)]
        # creates a copy of the current castle rights so when we append more for the log it will be the current one at that time


    """
    Takes a move as a parameter and executes it
    """

    def make_move(self, move):
        self.board[move.initial_row][move.first_file] = "E"
        self.board[move.last_row][move.last_file] = move.piece_moved
        self.move_log.append(move)  # log the move
        self.white_turn = not self.white_turn  # swap players
        # update king's position
        if move.piece_moved == "wK":
            self.white_king_location = (move.last_row, move.last_file)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.last_row, move.last_file)

        # pawn promotion
        if move.pawn_promotion_valid:
            if not self.white_turn:
                self.board[move.last_row][move.last_file] = "wQ"
            else:
                self.board[move.last_row][move.last_file] = "bQ"

        # castle move
        if move.is_castle_move:
            if move.last_file - move.first_file == 2:  # short castle
                self.board[move.last_row][move.last_file - 1] = self.board[move.last_row][
                    move.last_file + 1]  # moves the rook
                self.board[move.last_row][move.last_file + 1] = 'E'  # delete old rook
            else:  # long castle
                self.board[move.last_row][move.last_file + 1] = self.board[move.last_row][
                    move.last_file - 2]  # moves the rook
                self.board[move.last_row][move.last_file - 2] = 'E'  # delete old rook

        # update castling rights
        self.update_castling_rights(move)
        self.castle_rights_log.append(castle_rights(self.current_castle_rights.white_short,
                                                    self.current_castle_rights.white_long,
                                                    self.current_castle_rights.black_short,
                                                    self.current_castle_rights.black_long))

        # en passant
        if move.is_enpasssant_move:
            self.board[move.initial_row][move.last_file] = 'E'  # capturing the pawn when enpassant

        # update enpassant_possible
        if move.piece_moved[1] == 'p' and abs(move.initial_row - move.last_row) == 2:  # only on 2 square pawn advances
            self.enpassant_possible = ((move.initial_row + move.last_row)//2, move.first_file)  # double divide gives an integer rather than single divide gives decimal
        else:
            self.enpassant_possible = ()



    """
    Update the castling rights with move parameter
    """

    def update_castling_rights(self, move):
        if move.piece_moved == 'wK':  # if kings have moved then castling cant be done
            self.current_castle_rights.white_short = False
            self.current_castle_rights.white_long = False
        elif move.piece_moved == 'bK':
            self.current_castle_rights.black_short = False
            self.current_castle_rights.black_long = False
        elif move.piece_moved == 'wR':
            if move.initial_row == 7:
                if move.first_file == 7:  # right rook
                    self.current_castle_rights.black_short = False
                elif move.first_file == 0:  # left
                    self.current_castle_rights.black_long = False
        elif move.piece_moved == 'bR':
            if move.initial_row == 0:
                if move.first_file == 7:  # right rook
                    self.current_castle_rights.black_short = False
                elif move.first_file == 0:  # left
                    self.current_castle_rights.black_long = False

        # no castling if there is no rook
        if move.piece_captured == 'wR':
            if move.last_row == 7:
                if move.last_file == 0:
                    self.current_castle_rights.white_long = False
                if move.last_file == 7:
                    self.current_castle_rights.white_short = False
        if move.piece_captured == 'bR':
            if move.last_row == 0:
                if move.last_file == 0:
                    self.current_castle_rights.black_long = False
                if move.last_file == 7:
                    self.current_castle_rights.black_short = False


    """
    Undo the last move
    """

    def undo_move(self):
        if len(self.move_log) != 0:  # make sure there is a move to undo
            move_object = self.move_log.pop()
            self.board[move_object.initial_row][move_object.first_file] = move_object.piece_moved
            self.board[move_object.last_row][move_object.last_file] = move_object.piece_captured
            self.white_turn = not self.white_turn  # switching turns back
            # update king's position
            if move_object.piece_moved == "wK":
                self.white_king_location = (move_object.initial_row, move_object.first_file)
            elif move_object.piece_moved == "bK":
                self.black_king_location = (move_object.initial_row, move_object.first_file)

            # undo enpassant move
            if move_object.is_enpasssant_move:
                self.board[move_object.last_row][move_object.last_file] = "E"  # leave the destination square blank
                self.board[move_object.initial_row][move_object.last_file] = move_object.piece_captured  # putting enemy piece back
                self.enpassant_possible = (move_object.last_row, move_object.last_file)  # crucial piece to allow redoing en passant

            # undo a 2 square pawn advance
            if move_object.piece_moved[1] == 'p' and abs(move_object.initial_row - move_object.last_row) == 2:
                self.enpassant_possible = ()

            # undo castle rights
            self.castle_rights_log.pop()  # delete new castle rights from undoing move
            castle_rights = self.castle_rights_log[-1]  # set the current castle rights to the last one in the list
            self.current_castle_rights.white_short = castle_rights.white_short
            self.current_castle_rights.white_long = castle_rights.white_long
            self.current_castle_rights.black_short = castle_rights.black_short
            self.current_castle_rights.black_long = castle_rights.black_long

            # undo castle
            if move_object.is_castle_move:
                if move_object.last_file - move_object.first_file == 2:  # short castle
                    self.board[move_object.last_row][move_object.last_file+1] = self.board[move_object.last_row][move_object.last_file-1]
                    self.board[move_object.last_row][move_object.last_file-1] = 'E'
                else:
                    print(move_object.last_file)
                    self.board[move_object.last_row][move_object.last_file-2] = self.board[move_object.last_row][move_object.last_file+1]
                    self.board[move_object.last_row][move_object.last_file+1] = 'E'

    """
    All moves considering checks
    """

    def get_valid_moves(self):
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = castle_rights(self.current_castle_rights.white_short,
            self.current_castle_rights.white_long,
            self.current_castle_rights.black_short,
            self.current_castle_rights.black_long)  # copy of current castling rights
        # 1) Generate all possible moves
        moves = self.get_all_possible_moves()
        if self.white_turn:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)
        # 2) for each move, make the move
        for i in range(len(moves)-1, -1, -1):  # when removing from a list go backwards through that list
            self.make_move(moves[i])
            # 3) generate all enemy's moves

            # 4) for each of your opponent's moves, see if they attack your king
            self.white_turn = not self.white_turn  # have to change turn back as make_move() changes turn
            if self.in_check():
                # 5) if they do attack your king, not a valid move
                moves.remove(moves[i])
            self.white_turn = not self.white_turn  # change back so we can go back to before
            self.undo_move()  # goes back to normal and this also changes turn, so we go back to player's turn
        if len(moves) == 0:  # either checkmate or stalemate
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:  # when undoing moves make sure you still can if it was checkmate next move
            self.check_mate = False
            self.stale_mate = False

        self.enpassant_possible = temp_enpassant_possible  # keep enpassant move when undoing
        self.current_castle_rights = temp_castle_rights
        return moves

    """
    checks whichever players kings in check
    """

    def in_check(self):
        if self.white_turn:
            return self.square_under_attack(self.white_king_location[0],self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    """
    Determine if the enemy can attack the square r, c
    """

    def square_under_attack(self, row, file):
        self.white_turn = not self.white_turn  # switch to opponent's turn
        opp_moves = self.get_all_possible_moves()
        self.white_turn = not self.white_turn  # switch turns back
        for move in opp_moves:
            if move.last_row == row and move.last_file == file:  # square is under attack
                return True
        return False


    """
    All moves without considering checks
    """

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):  # number of rows
            for file in range(len(self.board[row])):  # number of files in given row
                turn = self.board[row][file][0]  # figures the color of the current players turn
                if (turn == 'w' and self.white_turn) or (turn == 'b' and not self.white_turn):
                    piece = self.board[row][file][1]  # gets the second letter of the item which is the piece type e.g. "bR" is a black rook
                    if piece == 'p':  # calls the appropriate move function based on piece type
                        self.get_pawn_moves(row, file, moves)
                    elif piece == 'N':
                        self.get_knight_moves(row, file, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(row, file, moves)
                    elif piece == 'R':
                        self.get_rook_moves(row, file, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(row, file, moves)
                    elif piece == 'K':
                        self.get_king_moves(row, file, moves)

        return moves


    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    """

    def get_pawn_moves(self, row, file, moves):
        if self.white_turn == True:  # white to move
            if self.board[row - 1][file] == "E":  # 1 square pawn advance
                moves.append(move((row, file), (row - 1, file), self.board))
            if row == 6 and self.board[row - 2][file] == "E" and self.board[row - 1][file] == "E":  # 2 square pawn advance
                moves.append(move((row, file), (row - 2, file), self.board))
            if file-1 >= 0:  # don't want to capture things outside the board
                # capture to the left
                if self.board[row - 1][file - 1][0] == 'b':  # capture the enemy piece
                    moves.append(move((row, file), (row - 1, file - 1), self.board))
                elif (row - 1, file - 1) == self.enpassant_possible:  # enpassant
                    moves.append(move((row, file), (row - 1, file - 1), self.board, enpassant_valid=True))  # similar to capture enemy piece but enpassant possible

            if file+1 <= 7:  # capture to the right
                if self.board[row - 1][file + 1][0] == 'b':  # capture the enemy piece
                    moves.append(move((row, file), (row - 1, file + 1), self.board))
                elif (row - 1, file + 1) == self.enpassant_possible:  # enpassant
                    moves.append(move((row, file), (row - 1, file + 1), self.board, enpassant_valid=True))

        # black pawn

        elif not self.white_turn:
            if self.board[row + 1][file] == "E":  # 1 square pawn advance
                moves.append(move((row, file), (row + 1, file), self.board))
            if row == 1 and self.board[row + 2][file] == "E" and self.board[row + 1][file] == "E":  # 2 square pawn advance
                moves.append(move((row, file), (row + 2, file), self.board))
            if file+1 <= 7:  # don't want to capture things outside the board
                # capture to the left black pov
                if self.board[row + 1][file + 1][0] == 'w':  # capture the enemy piece
                    moves.append(move((row, file), (row + 1, file + 1), self.board))
                elif (row + 1, file + 1) == self.enpassant_possible:  # enpassant
                    moves.append(move((row, file), (row + 1, file + 1), self.board, enpassant_valid=True))
            if file-1 >= 0:  # capture to the right black pov
                if self.board[row + 1][file - 1][0] == 'w':  # capture the enemy piece
                    moves.append(move((row, file), (row + 1, file - 1), self.board))
                elif (row + 1, file - 1) == self.enpassant_possible:  # enpassant
                    moves.append(move((row, file), (row + 1, file - 1), self.board, enpassant_valid=True))



        # pawn promotions later

    """
    Get all the rook moves for the rook located at row, col and add these moves to the list
    """

    def get_rook_moves(self, row, file, moves):
        directions_list = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        if self.white_turn:
            opp_colour = "b"
        else: opp_colour = "w"
        for i in directions_list:  # go through each direction
            count = 1  # running counter for each position after the piece
            while True:  # running a loop until it hits a friendly or enemy piece
                potential_row = row + i[0] * count  # after every loop goes one more in that direction
                potential_file = file + i[1] * count
                if 0 <= potential_row <= 7 and 0 <= potential_file <= 7:  # make sure not out of range
                    current_piece = self.board[potential_row][potential_file]
                    if current_piece == "E":  # empty space
                        moves.append(move((row, file), (potential_row, potential_file), self.board))
                    elif current_piece[0] == opp_colour:  # enemy piece but stop loop afterwards as you cant jump over pieces
                        moves.append(move((row, file), (potential_row, potential_file), self.board))
                        break
                    else:  # friendly piece so just break add no move
                        break
                else:  # out of bounds no longer valid position
                    break
                count = count + 1

    """
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    """

    def get_bishop_moves(self, row, file, moves):  # identical to get rook moves difference being directions
        directions_list = ((-1, -1), (-1,1), (1, -1), (1, 1))  # top left, bottom left, top right, bottom right
        opp_colour = "b" if self.white_turn else "w"
        for i in directions_list:  # go through each direction
            count = 1  # running counter for each position after the piece
            while True:  # running a loop until it hits a friendly or enemy piece
                potential_row = row + i[0] * count  # after every loop goes one more in that direction
                potential_file = file + i[1] * count
                if 0 <= potential_row <= 7 and 0 <= potential_file <= 7:
                    current_piece = self.board[potential_row][potential_file]
                    if current_piece == "E":  # empty space
                        moves.append(move((row, file), (potential_row, potential_file), self.board))
                    elif current_piece[
                        0] == opp_colour:  # enemy piece but stop loop afterwards as you cant jump over pieces
                        moves.append(move((row, file), (potential_row, potential_file), self.board))
                        break
                    else:  # friendly piece so just break add no move
                        break
                else:  # out of bounds no longer valid position
                    break
                count = count + 1


    """
    Get all the knight moves for the knight located at row, col and add these moves to the list
    """

    def get_knight_moves(self, row, file, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        friend_colour = "w" if self.white_turn else "b"
        for m in knight_moves:
            last_row = row + m[0]
            last_file = file + m[1]
            if 0 <= last_row < 8 and 0 <= last_file < 8:
                last_piece = self.board[last_row][last_file]
                if last_piece[0] != friend_colour:  # not an friendly piece empty or enemy piece)
                    moves.append(move((row, file), (last_row, last_file), self.board))

    """
    Get all the queen moves for the queen located at row, col and add these moves to the list
    """

    def get_queen_moves(self, row, file, moves):  # queen is essentially a rook and a bishop combined
        self.get_rook_moves(row, file, moves)
        self.get_bishop_moves(row, file, moves)

    """
    Get all the king moves for the king located at row, col and add these moves to the list
    """

    def get_king_moves(self, row, file, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        friend_colour = "w" if self.white_turn else "b"
        for i in range(8):
            last_row = row + king_moves[i][0]
            last_file = file + king_moves[i][1]
            if 0 <= last_row < 8 and 0 <= last_file < 8:
                last_piece = self.board[last_row][last_file]
                if last_piece[0] != friend_colour:  # not an ally piece (empty or enemy piece)
                    moves.append(move((row, file), (last_row, last_file), self.board))

    """
    Create all castle moves for king at given coordinates
    """
    def get_castle_moves(self, row, file, moves):
        if self.square_under_attack(row, file):
            return  # no castling when in check

        # short castle
        if (self.white_turn and self.current_castle_rights.white_short) or (not self.white_turn and self.current_castle_rights.black_short):
            if self.board[row][file + 1] == 'E' and self.board[row][file + 2] == 'E':  # make sure the spaces are clear
                if not self.square_under_attack(row, file + 1) and not self.square_under_attack(row, file + 2):  # make sure the squares arent under check
                    moves.append(move((row, file), (row, file + 2), self.board, castle_valid=True))

        # long castle
        if (self.white_turn and self.current_castle_rights.white_long) or (not self.white_turn and self.current_castle_rights.black_long):
            if self.board[row][file - 1] == 'E' and self.board[row][file - 2] == 'E' and self.board[row][file - 3] == 'E':  # make sure the spaces are clear
                if not self.square_under_attack(row, file - 1) and not self.square_under_attack(row, file - 2):  # make sure the squares arent under check
                    moves.append(move((row, file), (row, file - 2), self.board, castle_valid=True))

class castle_rights():
    def __init__(self, white_short, white_long, black_short, black_long):
        self.white_short = white_short
        self.white_long = white_long
        self.black_short = black_short
        self.black_long = black_long


class move():

    def __init__(self, first_sqr, last_sqr, board, enpassant_valid=False, castle_valid=False): # enpassant possible is an optional parameter used in some cases
        # enpassant possible is false so it won't work unless in the function call it is specified which makes it optional and quite useful
        self.initial_row = int(first_sqr[0])
        self.first_file = int(first_sqr[1])
        self.last_row = int(last_sqr[0])
        self.last_file = int(last_sqr[1])
        self.piece_moved = board[self.initial_row][self.first_file]
        self.piece_captured = board[self.last_row][self.last_file]
        # pawn promotion
        self.pawn_promotion_valid = False
        if (self.piece_moved == 'wp' and self.last_row == 0) or (self.piece_moved == 'bp' and self.last_row == 7):  # Flags up when pawn promotion is available
            self.pawn_promotion_valid = True
        # en passant
        self.is_enpasssant_move = enpassant_valid
        if self.is_enpasssant_move:
                if self.piece_moved == 'bp':
                    self.piece_captured = 'wp'
                else:
                    self.piece_captured = 'bp'
        # castle
        self.is_castle_move = castle_valid
        self.move_ID = self.initial_row*1000 + self.first_file *100 + self.last_row *10 + self.last_file  # essentially a hash function for each move between 0000 and 7777 needed for equals function so can decipher between pieces

    """
    Overriding the equals function, needed because we have a move class and they arent exactly the same the instance make sures its an object of move and this makes sures no piece can move in the same place by using move ids
    """

    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_ID == other.move_ID
        return False


    def get_chess_notation(self):  # gets notation from using the get coords function
        return self.get_coordinates(self.initial_row, self.first_file) + self.get_coordinates(self.last_row, self.last_file)

    def get_coordinates(self, r, f):  # assigns all chess notation to each position
        file = ""
        rank = ""

        if f == 0:
            file = "a"
        elif f == 1:
            file = "b"
        elif f == 2:
            file = "c"
        elif f == 3:
            file = "d"
        elif f == 4:
            file = "e"
        elif f == 5:
            file = "f"
        elif f == 6:
            file = "g"
        elif f == 7:
            file = "h"

        if r == 7:
            rank = "1"
        elif r == 6:
            rank = "2"
        elif r == 5:
            rank = "3"
        elif r == 4:
            rank = "4"
        elif r == 3:
            rank = "5"
        elif r == 2:
            rank = "6"
        elif r == 1:
            rank = "7"
        elif r == 0:
            rank = "8"

        return file + rank
