# Program by Jordan Oberstein
# Based on the the 1981 board game InnerCircle, (Milton Bradley company)

import random
import sys
import os
from colored import fg, bg, attr

from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4


COLORIZE_BOARD = True
HARD_MODE = False


def flatten(l): return [item for sublist in l for item in sublist]


RESET = fg(15)+bg(0)+attr(0)
def colorize(text, foreground, background, attribute):
    """Colorize text."""
    return fg(foreground)+bg(background)+attr(attribute)+text+RESET


class HiddenPrints:
    """Overides print function."""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class Display(object):
    def __init__(self, board, *args):
        """
        Constructor for Display class.

        Parameters:
            board: board to be displayed.
            *args: attributes in board data to be displayed.
        """
        self.board = board
        self.board_attributes = args

    def board_output(self):
        """Formats board data into readable output."""
        output = ""
        if len(self.board_attributes) == 0:
            output += "{:^120}{:^60}\n".format("(name, has_piece, dots)", "sub_dots")
            for row in self.board:
                new_line = str([(space["name"], space["has_piece"], space["dots"]) for space in row])
                new_line = new_line.replace("False,", "--,")  # False is default for has_piece
                new_line = new_line.replace("'", "")
                new_line = new_line.replace("), (", ") (")
                sub_dots = str(["?" if HARD_MODE and space["has_piece"] and space["is_hole"] else space["sub_dots"] for space in row])
                sub_dots = sub_dots.replace("False", "-")
                sub_dots = sub_dots.replace("'", "")
                output += "{:^120}{:^60}\n".format(new_line, sub_dots)
            if HARD_MODE:
                for player in range(1, 19):
                    for dots in range(1, 5):
                        output = output.replace("P{}, {}".format(player, dots), "P{}, ?".format(player))
            if COLORIZE_BOARD:
                output = output.replace("P1,", colorize("P1", 1, 0, 4) + ",")  # Red
                output = output.replace("P2", colorize("P2", 2, 0, 4))  # Green
                output = output.replace("P3", colorize("P3", 4, 0, 4))  # Blue
                output = output.replace("P4", colorize("P4", 3, 0, 4))  # Yellow
                output = output.replace("P5", colorize("P5", 124, 0, 4))  # Red
                output = output.replace("P6", colorize("P6", 114, 0, 4))  # Green
                output = output.replace("P7", colorize("P7", 104, 0, 4))  # Blue
                output = output.replace("P8", colorize("P8", 94, 0, 4))   # Yellow
                output = output.replace("C", colorize("C", 0, 7, 1))  # White bg
                output = output.replace("H", colorize("H", 0, 5, 1))  # Purple bg
        else:
            for attribute in self.board_attributes:
                output += "{:^60}".format(attribute)
            output += "\n"
            for row in self.board:
                for attribute in self.board_attributes:
                    output += "{:^60}".format(str([space[attribute] for space in row]))
                output += "\n"
        return output

    def __str__(self):
        """Print board data."""
        return self.board_output()

    def retrieve_attr_data(self):
        """Retrieves data for board arguments in initialization."""
        return (*[[[space[attribute] for space in row] for row in self.board] for attribute in self.board_attributes],)


class Actions(object):
    def __init__(self, board):
        """Constructor for Actions class."""
        self.board = board

    def rotate(self, r):
        """Rotate a board r rotations counterclockwise."""
        old_board = self.board
        ring_1 = [old_board[2][2], old_board[2][3], old_board[3][4], old_board[4][3], old_board[4][2], old_board[3][2]]
        ring_2 = [old_board[1][1], old_board[1][2], old_board[1][3], old_board[2][4], old_board[3][5], old_board[4][4],
                  old_board[5][3], old_board[5][2], old_board[5][1], old_board[4][1], old_board[3][1], old_board[2][1]]
        ring_3 = [old_board[0][0], old_board[0][1], old_board[0][2], old_board[0][3], old_board[1][4], old_board[2][5],
                  old_board[3][6], old_board[4][5], old_board[5][4], old_board[6][3], old_board[6][2], old_board[6][1],
                  old_board[6][0], old_board[5][0], old_board[4][0], old_board[3][0], old_board[2][0], old_board[1][0]]

        # Rotate each ring
        inner_ring = ring_1[-r:] + ring_1[:-r]
        middle_ring = ring_2[-2*r:] + ring_2[:-2*r]
        outer_ring = ring_3[-3*r:] + ring_3[:-3*r]

        new_board = [[0]*4, [0]*5, [0]*6, [0]*7, [0]*6, [0]*5, [0]*4]
        new_board[2][2], new_board[2][3], new_board[3][4], new_board[4][3], new_board[4][2], new_board[3][2] = inner_ring
        (new_board[1][1], new_board[1][2], new_board[1][3], new_board[2][4], new_board[3][5], new_board[4][4],
         new_board[5][3], new_board[5][2], new_board[5][1], new_board[4][1], new_board[3][1], new_board[2][1]) = middle_ring
        (new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3], new_board[1][4], new_board[2][5],
         new_board[3][6], new_board[4][5], new_board[5][4], new_board[6][3], new_board[6][2], new_board[6][1],
         new_board[6][0], new_board[5][0], new_board[4][0], new_board[3][0], new_board[2][0], new_board[1][0]) = outer_ring
        new_board[3][3] = old_board[3][3]
        return new_board

    def find_correct_space(self, piece):
        """Determines correct space based on name of piece, required when board is rotated and index doesn't match name."""
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y]["name"] == piece:
                    return "i{}{}".format(x, y)

    def legal_moves(self, piece):
        """Determines legal moves for a given piece."""
        x = int(piece[1])  # Row
        y = int(piece[2])  # Collumn
        legal_spaces = self.board[x][y]["moves_to"]
        legal_spaces_without_pieces = []
        for space in legal_spaces:
            piece_index = self.find_correct_space(space)
            if not self.board[int(piece_index[1])][int(piece_index[2])]["has_piece"]:
                legal_spaces_without_pieces.append(space)
        return legal_spaces_without_pieces

    def take_turn_random(self, CP_pieces, CP_name):
        """Execute turn for player through random choice."""
        center_name = "i33"
        if center_name in CP_pieces:
            piece = center_name
            piece_index = center_name
            print(CP_name, "has a piece in the center...")
        else:
            unblocked_pieces = [a_piece for a_piece in CP_pieces if len(self.legal_moves(self.find_correct_space(a_piece))) > 0]
            print("Available pieces:", CP_pieces)
            print("Unblocked_pieces:", unblocked_pieces)
            if len(unblocked_pieces) == 0:
                print(CP_name, "has no available pieces. All pieces are blocked")
                return False
            piece = random.choice(unblocked_pieces)
            piece_index = self.find_correct_space(piece)
        dots = self.board[int(piece_index[1])][int(piece_index[2])]["dots"]
        legal_spaces = self.legal_moves(piece_index)
        selected_move = random.choice(legal_spaces)
        selected_move_index = self.find_correct_space(selected_move)
        print("Selected piece from list:", piece)
        print("Selected piece has index:", piece_index)
        print("Piece at index {} moves {} spaces".format(piece_index, dots))
        print("Legal spaces:", legal_spaces)
        print("Selected move from list:", selected_move)
        print("Selected move has index:", selected_move_index)
        x0 = int(piece_index[1])
        y0 = int(piece_index[2])
        x1 = int(selected_move_index[1])
        y1 = int(selected_move_index[2])
        self.board[x0][y0]["has_piece"] = False
        self.board[x1][y1]["has_piece"] = CP_name

    def take_turn(self, CP_pieces, CP_name):
        """Execute turn for player through user's choice."""
        center_name = "i33"
        legal_spaces = []
        available_pieces = CP_pieces.copy()
        if center_name in CP_pieces:
            piece = center_name
            piece_index = center_name
            dots = self.board[int(piece_index[1])][int(piece_index[2])]["dots"]  # "C"
            legal_spaces = self.legal_moves(piece_index)
            print(CP_name, "has a piece in the center...")
        else:
            while len(legal_spaces) == 0:
                print("Available pieces:", available_pieces)
                selected_piece = input("These are the available pieces for {}... {}:\n==> ".format(CP_name, available_pieces))
                while not selected_piece.isdigit() or int(selected_piece) >= len(available_pieces):
                    selected_piece = input("These are the available pieces for {}... {}:\n==> ".format(CP_name, available_pieces))
                piece = available_pieces[int(selected_piece)]
                piece_index = self.find_correct_space(piece)
                dots = self.board[int(piece_index[1])][int(piece_index[2])]["dots"]
                legal_spaces = self.legal_moves(piece_index)
                print("Piece at index {} moves {} spaces".format(piece_index, dots))
                print("Legal spaces:", legal_spaces)
                if len(legal_spaces) == 0:
                    print("Selected piece is blocked")
                    if HARD_MODE:
                        return False
                    available_pieces.remove(piece)
                    if len(available_pieces) == 0:
                        print(CP_name, "has no available pieces; all pieces are blocked")
                        return False
        selected_legal_space = input("These are the available moves for piece {}... {}:\n==> ".format(piece, legal_spaces))
        while not selected_legal_space.isdigit() or int(selected_legal_space) >= len(legal_spaces):
            selected_legal_space = input("These are the available moves for piece {}... {}:\n==> ".format(piece, legal_spaces))
        selected_move = legal_spaces[int(selected_legal_space)]
        selected_move_index = self.find_correct_space(selected_move)
        print("Selected piece from list:", piece)
        print("Selected piece has index:", piece_index)
        print("Piece at index {} moves {} spaces".format(piece_index, dots))
        print("Legal spaces:", legal_spaces)
        print("Selected move from list:", selected_move)
        print("Selected move has index:", selected_move_index)
        x0 = int(piece_index[1])
        y0 = int(piece_index[2])
        x1 = int(selected_move_index[1])
        y1 = int(selected_move_index[2])
        self.board[x0][y0]["has_piece"] = False
        self.board[x1][y1]["has_piece"] = CP_name


class Players(object):
    def __init__(self, player_count):
        """
        Constructor for Player class.

        Parameters:
            player_count: the number of players playing the game int in range(2, 19).
        """
        self.player_count = player_count
        self.players = {"P{}".format(n): {"pieces": [], "is_active": True} for n in range(1, self.player_count + 1)}

    def get_active_players(self):
        """Update active players."""
        return [player for player in self.players if self.players[player]["is_active"]]

    def update_players(self, board):
        """Update player object."""
        active_players = self.get_active_players()
        for player in active_players:
            self.players[player]["pieces"] = [space["name"] for space in flatten(board) if space["has_piece"] == player and not space["is_hole"]]

    def update_player_status(self, board):
        """Update player object when moving down boards, removing eliminated players."""
        active_players = self.get_active_players()
        for player in active_players:
            self.players[player]["pieces"] = [space["name"] for space in flatten(board) if space["has_piece"] == player]
            if len(self.players[player]["pieces"]) == 0:
                self.players[player]["is_active"] = False

    def remove_inactive_players(self, starting_spaces_length):
        """Remove players when the number of players is greater than the number of starting spaces."""
        if self.player_count > starting_spaces_length:
            for player in self.players:
                player_number = int(player[1:])
                if player_number > starting_spaces_length:
                    self.players[player]["is_active"] = False


class NewGame(object):
    def __init__(self, top_board, player_count, random_gameplay):
        """
        Constructor for NewGame class.

        Parameters:
            board: the top board for gameplay (B4, B3, B2, B1).
            player_count: the number of players playing the game int in range(2, 19).
            random_gameplay: will gameplay will be executed through random choice or user input.
        """
        self.board = top_board
        self.board_array = [B4, B3, B2, B1][[B4, B3, B2, B1].index(self.board):]  # List of boards being used
        self.player_count = player_count
        self.players = Players(self.player_count)
        self.random_gameplay = random_gameplay
        self.turn = 1
        self.winner = False

    def configure_boards(self):
        """Rotate boards in board_array, then add sub_dots."""
        for i in range(1, len(self.board_array)):
            r = random.randint(0, 5)
            self.board_array[i] = Actions(self.board_array[i]).rotate(r)
            upper_board = self.board_array[i-1]
            lower_board = self.board_array[i]
            for x in range(len(upper_board)):
                for y in range(len(upper_board[x])):
                    if upper_board[x][y]["is_hole"]:
                        upper_board[x][y]["sub_dots"] = lower_board[x][y]["dots"]

    def get_starting_spaces(self):
        """Get starting spaces and determine pieces per player."""
        if self.board == B4:
            starting_spaces = [space["name"] for space in flatten(self.board) if space["starting_space"]]
            random.shuffle(starting_spaces)
            equal_spaces = (18//self.player_count)*self.player_count
            starting_spaces = starting_spaces[:equal_spaces]
        else:
            r = random.randint(0, 5)
            upper_board = B2 if self.board == B1 else (B3 if self.board == B2 else B4)
            flat_upper_board = flatten(Actions(upper_board).rotate(r))
            flat_starting_board = flatten(self.board)
            starting_spaces = [starting_board["name"] for starting_board,upper_board in zip(flat_starting_board, flat_upper_board) if upper_board["is_hole"]]
            random.shuffle(starting_spaces)
        self.starting_spaces_length = len(starting_spaces)
        number_of_separations = min(self.starting_spaces_length, self.player_count)
        minimum_pieces, extra_piece = divmod(self.starting_spaces_length, self.player_count)
        separations = [minimum_pieces + (1 if i<extra_piece else 0) for i in range(number_of_separations)]
        random.shuffle(separations)
        return starting_spaces, separations

    def configure_players_random(self):
        """Configure player object for random gameplay."""
        starting_spaces, pieces_per_player = self.get_starting_spaces()
        self.players.remove_inactive_players(self.starting_spaces_length)
        active_players = self.players.get_active_players()
        player_names = [player for player,total_pieces in zip(active_players, pieces_per_player) for i in range(total_pieces)]
        for name,space in zip(player_names, starting_spaces):
            self.board[int(space[1])][int(space[2])]["has_piece"] = name
        self.players.update_players(self.board)

    def configure_players(self):
        """Configure player object for user-selected gameplay"""
        starting_spaces, pieces_per_player = self.get_starting_spaces()
        self.players.remove_inactive_players(self.starting_spaces_length)
        active_players = self.players.get_active_players()
        extra_pieces = [player for player,total_pieces in zip(active_players, pieces_per_player) if total_pieces > min(pieces_per_player)]
        player_names = active_players*min(pieces_per_player) + extra_pieces
        #player_names = flatten([[player for player,total_pieces in zip(active_players, pieces_per_player) if i < total_pieces] for i in range(max(pieces_per_player))])
        print("player names:", player_names)  # Order that players place pieces
        for name in player_names:
            print("Pick a space for", name)
            space_index = input("These are the remaining spaces... {}\n==> ".format(starting_spaces))
            while not space_index.isdigit() or int(space_index) >= self.starting_spaces_length:
                space_index = input("These are the remaining spaces... {}\n==> ".format(starting_spaces))
            selected_space = starting_spaces.pop(int(space_index))
            x = int(selected_space[1])  # Row
            y = int(selected_space[2])  # Collumn
            self.board[x][y]["has_piece"] = name
            self.players.update_players(self.board)
            print(Display(self.board))

    def make_move_random(self):
        """Make random move for player."""
        center = self.board[3][3]
        if not center["has_piece"]:
            active_players = self.players.get_active_players()
            self.CP_name = "P1" if self.turn == 1 else active_players[(active_players.index(self.CP_name)+1) % len(active_players)]
        self.CP_pieces = self.players.players[self.CP_name]["pieces"]  # Wrong player if game starts with piece in center
        print(self.CP_name, "has these pieces:", self.CP_pieces)
        if len(self.CP_pieces) == 0:
            print(self.CP_name, "has no valid moves")
        else:
            Actions(self.board).take_turn_random(self.CP_pieces, self.CP_name)

    def make_move(self):
        """Make move for player."""
        center = self.board[3][3]
        if not center["has_piece"]:
            active_players = self.players.get_active_players()
            self.CP_name = "P1" if self.turn == 1 else active_players[(active_players.index(self.CP_name)+1) % len(active_players)]
        self.CP_pieces = self.players.players[self.CP_name]["pieces"]  # Wrong player if game starts with piece in center
        print(self.CP_name, "has these pieces:", self.CP_pieces)
        if len(self.CP_pieces) == 0:
            print(self.CP_name, "has no valid moves")
        else:
            Actions(self.board).take_turn(self.CP_pieces, self.CP_name)

    def check_for_winner(self):
        """Check for winner."""
        center = self.board[3][3]
        active_players = self.players.get_active_players()
        if (len(self.board_array) == 1 and center["has_piece"]) or len(active_players) == 1:
            self.winner = self.CP_name  # Player who moves into center or last remaining player
        return self.winner

    def imprint_board(self):
        """Assigns pieces in holes to lower board."""
        next_board = self.board_array[1]
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y]["is_hole"]:
                    next_board[x][y]["has_piece"] = self.board[x][y]["has_piece"]
        self.board_array.pop(0)
        self.board = self.board_array[0]  # self.board is now next board in self.board_array
        print("\n\n\nALL HOLES ARE FILLED ON BOARD B{}; NOW MOVING TO BOARD B{}\n\n\n".format(len(self.board_array)+1, len(self.board_array)))

    def play(self):
        """Play a complete game."""
        print(Display(self.board))
        self.configure_boards()
        if self.random_gameplay:
            self.configure_players_random()
        else:
            self.configure_players()
        print("Game Setup is now complete")

        while True:
            break
            print("\n\n\nTURN NUMBER", self.turn)
            print(Display(self.board))
            self.players.update_players(self.board)
            if self.random_gameplay:
                self.make_move_random()
            else:
                self.make_move()

            center = self.board[3][3]
            if center["has_piece"]:
                print(Display(self.board))
                self.players.update_players(self.board)
                if self.check_for_winner():
                    break
                if self.random_gameplay:
                    self.make_move_random()
                else:
                    self.make_move()

            # Check if all pieces are in holes
            if all([space["has_piece"] for space in flatten(self.board) if space["is_hole"]]):
                print(Display(self.board))
                self.imprint_board()
                self.players.update_player_status(self.board)
                if self.check_for_winner():
                    break

            self.turn += 1

        if self.winner:
            print("\n\nThere is a winner...")
            print(Display(self.board))
            print("\nTHE WINNER IS", self.winner)
        else:
            print("\n\nGame incomplete.")
            print(Display(self.board))


def main():
    with open("out.txt", "w") as outfile:
        pass

    TOP_BOARD = B4
    PLAYER_COUNT = 18
    RANDOM_GAMEPLAY = True
    PRINT_TO_CONSOLE = True

    if TOP_BOARD not in [B4, B3, B2, B1]:
        raise ValueError("Only (B4, B3, B2, B1) are allowed")
    if PLAYER_COUNT not in range(2, 19):
        raise ValueError("Valid input is int in range(2, 19)")
    if type(RANDOM_GAMEPLAY) is not bool:
        raise ValueError("Valid input is bool")

    Game = NewGame(TOP_BOARD, PLAYER_COUNT, RANDOM_GAMEPLAY)

    if PRINT_TO_CONSOLE:
        Game.play()
    else:
        with HiddenPrints():
            Game.play()


if __name__ == "__main__":
    main()


"""
TO-DO:
Expand and clarify docstrings
Create GUI

IDEAS:
Create move trees and determine winning strategy
Create AI to learn game, find optimal strategy

DIFFERENCES FROM MAIN GAME:
- can support more than four players
- has easy mode where player's turn isn't skipped if you choose a blocked piece
"""
