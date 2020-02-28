#Program by Jordan Oberstein
#Based on the the 1981 board game InnerCircle, (Milton Bradley company, board game originally designed by Virginia Charves)

import random
import sys, os
from colored import fg, bg, attr

from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4


colorize_board = True
print_to_console = True
random_gameplay = True
hard_mode = False


flatten = lambda l: [item for sublist in l for item in sublist]

def colorize(text, foreground, background, attribute):
	"""Colorizes text."""
	return "{}{}{}{}{}{}{}".format(fg(foreground), bg(background), attr(attribute), text, fg(15), bg(0), attr(0))

class HiddenPrints:
	"""Overides print function."""
	def __enter__(self):
		self._original_stdout = sys.stdout
		sys.stdout = open(os.devnull, 'w')
	def __exit__(self, exc_type, exc_val, exc_tb):
		sys.stdout.close()
		sys.stdout = self._original_stdout


class Display(object):
	def __init__(self, board, board_attributes=[]):
		""" 
		Constructor for Display class. 

		Parameters: 
			board: board to be displayed.
			board_attributes: (optional) specific arguments in board data to be displayed. 
		"""
		self.board = board
		self.board_attributes = board_attributes

	def board_output(self):
		"""Formats board data into readable output."""
		DATA = ""
		if len(self.board_attributes) == 0:
			DATA += "{:^120}{:^60}\n".format("(name, has_piece, dots)", "sub_dots")
			for row in self.board:
				new_line = str([(space["name"], space["has_piece"], space["dots"]) for space in row])
				new_line = new_line.replace("False,", "--,") #has_piece
				new_line = new_line.replace("'", "") #flush formatting
				new_line = new_line.replace("), (", ") (") #flush formatting
				sub_dots = str([space["sub_dots"] for space in row])
				sub_dots = sub_dots.replace("False", "-")
				DATA += "{:^120}{:^60}\n".format(new_line, sub_dots)
			if hard_mode:
				for player in range(1, 19):
					for dots in range(1, 5):
						DATA = DATA.replace("P{}, {}".format(player, dots), "P{}, ?".format(player))
			if colorize_board:
				DATA = DATA.replace("P1,", colorize("P1", 1, 0, 4) + ",") #red
				DATA = DATA.replace("P2", colorize("P2", 2, 0, 4)) #green
				DATA = DATA.replace("P3", colorize("P3", 4, 0, 4)) #blue
				DATA = DATA.replace("P4", colorize("P4", 3, 0, 4)) #yellow
				DATA = DATA.replace("C", colorize("C", 0, 7, 1)) #white bg
				DATA = DATA.replace("H", colorize("H", 0, 5, 1)) #purple bg
		else:
			for attr in self.board_attributes:
				DATA += "{:^60}".format(attr)
			DATA += "\n"
			for row in self.board:
				for attr in self.board_attributes:
					DATA += "{:^60}".format(str([space[attr] for space in row]))
				DATA += "\n"
		return DATA

	def __str__(self):
		"""__str__ method to print board data."""
		return self.board_output()

	def retrieve_attribute_data(self):
		return (*[[[space[attr] for space in row] for row in self.board] for attr in self.board_attributes],)


class Actions(object):
	def __init__(self, board):
		"""Constructor for Actions class."""
		self.board = board

	def rotate(self, r):
		"""Rotate a board r rotations counterclockwise."""
		old_board = self.board #prevents self.board from being overwritten by one sextant
		ring_1 = [old_board[2][2], old_board[2][3], old_board[3][4], old_board[4][3], old_board[4][2], old_board[3][2]]
		ring_2 = [old_board[1][1], old_board[1][2], old_board[1][3], old_board[2][4], old_board[3][5], old_board[4][4], \
			old_board[5][3], old_board[5][2], old_board[5][1], old_board[4][1], old_board[3][1], old_board[2][1]]
		ring_3 = [old_board[0][0], old_board[0][1], old_board[0][2], old_board[0][3], old_board[1][4], old_board[2][5], \
			old_board[3][6], old_board[4][5], old_board[5][4], old_board[6][3], old_board[6][2], old_board[6][1], \
			old_board[6][0], old_board[5][0], old_board[4][0], old_board[3][0], old_board[2][0], old_board[1][0]]
		
		#rotate each ring
		R1 = ring_1[-r:] + ring_1[:-r]
		R2 = ring_2[-2*r:] + ring_2[:-2*r]
		R3 = ring_3[-3*r:] + ring_3[:-3*r]
		center = old_board[3][3]

		new_board = [[0]*4, [0]*5, [0]*6, [0]*7, [0]*6, [0]*5, [0]*4]
		new_board[2][2], new_board[2][3], new_board[3][4], new_board[4][3], new_board[4][2], new_board[3][2] = R1[0], R1[1], R1[2], R1[3], R1[4], R1[5]
		new_board[1][1], new_board[1][2], new_board[1][3], new_board[2][4], new_board[3][5], new_board[4][4] = R2[0], R2[1], R2[2], R2[3], R2[4], R2[5]
		new_board[5][3], new_board[5][2], new_board[5][1], new_board[4][1], new_board[3][1], new_board[2][1] = R2[6], R2[7], R2[8], R2[9], R2[10], R2[11]
		new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3], new_board[1][4], new_board[2][5] = R3[0], R3[1], R3[2], R3[3], R3[4], R3[5]
		new_board[3][6], new_board[4][5], new_board[5][4], new_board[6][3], new_board[6][2], new_board[6][1] = R3[6], R3[7], R3[8], R3[9], R3[10], R3[11]
		new_board[6][0], new_board[5][0], new_board[4][0], new_board[3][0], new_board[2][0], new_board[1][0] = R3[12], R3[13], R3[14], R3[15], R3[16], R3[17]
		new_board[3][3] = center
		return new_board

	def find_correct_space(self, piece):
		"""Determines correct space based on name of piece, required when board is rotated and index doesn't match name."""
		for x in range(len(self.board)):
			for y in range(len(self.board[x])):
				if self.board[x][y]["name"] == piece:
					return "i{}{}".format(x, y)

	def legal_moves(self, piece):
		"""Determines legal moves for a given piece."""
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		dots = self.board[x][y]["dots"]
		print("Piece {} moves {} spaces".format(piece, dots))
		legal_spaces = self.board[x][y]["moves_to"]
		legal_spaces_without_pieces = []
		for space in legal_spaces:
			piece_index = self.find_correct_space(space)
			if not self.board[int(piece_index[1])][int(piece_index[2])]["has_piece"]:
				legal_spaces_without_pieces.append(space)
		return legal_spaces_without_pieces

	def take_turn(self, CP_pieces, CP_name):
		"""Execute turn for current player."""
		center_name = "i33"
		legal_spaces = []
		available_pieces = CP_pieces.copy()
		if center_name in CP_pieces:
			piece = center_name
			piece_index = center_name
			legal_spaces = self.legal_moves(piece)
		else:
			while len(legal_spaces) == 0: #will not continue unless the chosen piece has legal moves
				print("Checking for moves...")
				if len(available_pieces) == 0:
					print("{} has no available pieces, all pieces are blocked".format(CP_name))
					return False
				print("Available pieces: {}".format(available_pieces))
				if random_gameplay:
					piece_index = random.randint(0, len(available_pieces) - 1)
				else:
					piece_index = input("These are the available pieces (not already in holes) for {}, choose 1: {}:\n==> ".format(CP_name, available_pieces))
					while not piece_index.isdigit() or int(piece_index) >= len(available_pieces):
						piece_index = input("These are the available pieces (not already in holes) for {}, choose 1: {}:\n==> ".format(CP_name, available_pieces))
				piece = available_pieces[int(piece_index)]
				print("Selected piece from list is piece {}".format(piece))
				piece_index = self.find_correct_space(piece)
				print("Selected piece rotates into index {}".format(piece_index))
				available_pieces.remove(piece)
				legal_spaces = self.legal_moves(piece_index)
				if len(legal_spaces) == 0:
					print("Selected piece is blocked")
					if hard_mode:
						return False

		print("Legal spaces: {}".format(legal_spaces))
		if random_gameplay:
			legal_spaces_index = random.randint(0, len(legal_spaces) - 1)
		else:
			legal_spaces_index = input("These are the available moves for piece {}, choose 1: {}:\n==> ".format(piece, legal_spaces))
			while not legal_spaces_index.isdigit() or int(legal_spaces_index) >= len(legal_spaces):
				legal_spaces_index = input("These are the available moves for piece {}, choose 1: {}:\n==> ".format(piece, legal_spaces))
		selected_move = legal_spaces[int(legal_spaces_index)]
		x0 = int(piece_index[1]) #old row index
		y0 = int(piece_index[2]) #old collumn index
		print("Selected piece's index is: ({}, {})".format(x0, y0))
		print("Selected move from list is: ({}, {})".format(selected_move[1], selected_move[2]))
		selected_move_index = self.find_correct_space(selected_move)
		x1 = int(selected_move_index[1]) #new row index
		y1 = int(selected_move_index[2]) #new collumn index
		print("Selected move's index is: ({}, {})".format(x1, y1))
		self.board[x0][y0]["has_piece"] = False
		self.board[x1][y1]["has_piece"] = CP_name


class FullGame(object):
	def __init__(self, board, player_count):
		""" 
		Constructor for FullGame class. 

		Parameters: 
			board: the top board for gameplay (B1, B2, B3, B4). 
			player_count: the number of players playing the game int in range(2, 19). 
		"""
		self.board = board
		self.board_array = [B4, B3, B2, B1][[B4, B3, B2, B1].index(self.board):] #define board_array as list of boards being used
		self.player_count = player_count
		self.players = {"P{}".format(n): {"pieces":[], "is_active": True} for n in range(1, self.player_count + 1)}
		self.turn = 1
		self.winner = False

	def get_active_players(self):
		return [player for player in self.players if self.players[player]["is_active"]]

	def setup_game(self):
		"""Setup game (configure boards and player object)."""

		#rotate boards, add sub_dots
		for i in range(1, len(self.board_array)):
			r = random.randint(0,5)
			self.board_array[i] = Actions(self.board_array[i]).rotate(r) #rotate boards
			upper_board = self.board_array[i-1]
			lower_board = self.board_array[i]
			for x in range(len(upper_board)):
				for y in range(len(upper_board[x])):
					if upper_board[x][y]["is_hole"]:
						upper_board[x][y]["sub_dots"] = lower_board[x][y]["dots"]

		#add pieces to board, add pieces to each player in player object
		if self.board == B4:
			active_players = self.get_active_players()
			player_count = len(active_players)
			max_turns = (18//player_count)*player_count #equal number of starting pieces for each player
			for turn in range(1, max_turns + 1):
				print(Display(self.board))
				CP_name = active_players[turn%player_count - 1]
				remaining_spaces = [space["name"] for space in flatten(self.board) if space["starting_space"] and not space["has_piece"]]
				if random_gameplay:
					space_index = random.randint(0, len(remaining_spaces) - 1)
				else:
					space_index = input("These are the remaining spaces, choose 1: {}\n==> ".format(remaining_spaces))
					while not space_index.isdigit() or int(space_index) >= len(remaining_spaces):
						space_index = input("These are the remaining spaces, choose 1: {}\n==> ".format(remaining_spaces))
				chosen_space = remaining_spaces[int(space_index)]
				x = int(chosen_space[1]) #row
				y = int(chosen_space[2]) #collumn
				self.board[x][y]["has_piece"] = CP_name
			print(Display(self.board))
			print("Game Setup is complete.\n\n\n")
		else:
			#determine starting spaces
			r = random.randint(0,5)
			upper_board = B2 if self.board == B1 else (B3 if self.board == B2 else B4)
			flat_upper_board = flatten(Actions(upper_board).rotate(r))
			flat_starting_board = flatten(self.board)
			starting_spaces = [item[0]["name"] for item in zip(flat_starting_board, flat_upper_board) if item[1]["is_hole"]]
			random.shuffle(starting_spaces)

			#determine cuts in starting spaces 
			separations = [0]*self.player_count
			for i in range(len(starting_spaces)):
				separations[i%self.player_count] += 1
			separations = [num for num in separations if num != 0]
			random.shuffle(separations)
			cuts = [sum(separations[:n]) for n in range(0, len(separations) + 1)]

			#remove players who are eliminated due to not having enough spaces
			if self.player_count > len(starting_spaces):
				for player in self.players:
					if int(player[1:]) > len(starting_spaces):
						self.players[player]["is_active"] = False

			#add pieces to players object, add pieces to board
			active_players = self.get_active_players()
			for n in range(len(active_players)):
				player = active_players[n]
				self.players[player]["pieces"] = starting_spaces[cuts[n]:cuts[n+1]]
				print(player, self.players[player]["pieces"])
				for space in self.players[player]["pieces"]:
					self.board[int(space[1])][int(space[2])]["has_piece"] = player

	def update_players(self):
		"""Update player object."""
		active_players = self.get_active_players()
		for player in active_players:
			self.players[player]["pieces"] = [space["name"] for space in flatten(self.board) if space["has_piece"] == player and not space["is_hole"]]

	def update_player_status(self):
		"""Update player object when moving down boards, removing eliminated players."""
		active_players = self.get_active_players()
		for player in active_players:
			self.players[player]["pieces"] = [space["name"] for space in flatten(self.board) if space["has_piece"] == player]
			if len(self.players[player]["pieces"]) == 0:
				self.players[player]["is_active"] = False

	def make_move(self):
		center = self.board[3][3]
		if not center["has_piece"]:
			active_players = self.get_active_players()
			self.CP_name = "P1" if self.turn == 1 else active_players[(active_players.index(self.CP_name)+1)%len(active_players)] #checks index before assignment
			self.CP_pieces = self.players[self.CP_name]["pieces"]
			print(self.CP_name, self.CP_pieces)
		else:
			self.CP_pieces = self.players[self.CP_name]["pieces"]
			print("\n{}'s piece is in the center, they will now move it...\n".format(self.CP_name))
			print(Display(self.board))

		if len(self.CP_pieces) == 0:
			print("{} has no valid moves".format(self.CP_name))
			self.turn += 1
			return False
		else:
			Actions(self.board).take_turn(self.CP_pieces, self.CP_name)

	def check_for_winner(self):
		"""Check for winner."""
		center = self.board[3][3]
		active_players = self.get_active_players()
		if len(self.board_array) == 1 and center["has_piece"]:
			self.winner = center["has_piece"]
		elif len(active_players) == 1:
			self.winner = active_players[0]
		return self.winner #default False unless reassigned here

	def imprint_board(self):
		"""Assigns pieces in holes to lower board."""
		print(Display(self.board))
		next_board = self.board_array[1]
		for x in range(len(self.board)): #row
			for y in range(len(self.board[x])): #collumn
				if self.board[x][y]["has_piece"] and self.board[x][y]["is_hole"]:
					next_board[x][y]["has_piece"] = self.board[x][y]["has_piece"]
		self.board_array.pop(0)
		self.board = self.board_array[0] #self.board is now next board in self.board_array
		print("\n\n\nALL SPACES ON BOARD B{} ARE FILLED, MOVING DOWN TO BOARD B{}\n\n\n".format(len(self.board_array)+1, len(self.board_array)))

	def play(self):
		"""Play a complete game."""
		self.setup_game()
		while True:
			print("\n\n\nTURN NUMBER {}".format(self.turn))
			print(Display(self.board))
			self.update_players()
			self.make_move()

			center = self.board[3][3]
			if center["has_piece"]:
				if self.check_for_winner():
					break
				self.update_players()
				self.make_move()

			#check if all pieces are in holes
			if all([space["has_piece"] for space in flatten(self.board) if space["is_hole"]]):
				self.imprint_board()
				self.update_player_status()
				if self.check_for_winner():
					break

			self.turn += 1

	def get_winner(self):
		print("\n\nThere is a winner...")
		print(Display(self.board))
		print("\n\nTHE WINNER IS: {}".format(self.winner))
		return self.winner


def main():
	with open("out.txt", "w") as outfile:
		pass

	top_board = B4
	player_count = 2

	if player_count not in range(2, 19):
		raise ValueError("Valid input is int in range(2, 19)")
	if top_board not in [B1, B2, B3, B4]:
		raise ValueError("Only (B1, B2, B3, B4) are allowed")

	NewGame = FullGame(top_board, player_count)

	if print_to_console:
		NewGame.play()
	else:
		with HiddenPrints():
			NewGame.play()

	NewGame.get_winner()


if __name__ == "__main__":
	main()


"""
TO-DO:
Expand and clarify docstrings
Add proper reset method instead of using loop in seperate file to execute file multiple times

IDEAS:
Create GUI
Create move trees and determine winning strategy
Create AI to learn game, find optimal strategy

DIFFERENCES FROM MAIN GAME:
- supports more than four players
- allows you to choose a new move if you choose a move where all pieces are blocked
"""
