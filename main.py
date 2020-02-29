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
hard_mode = False


flatten = lambda l: [item for sublist in l for item in sublist]

reset = fg(15)+bg(0)+attr(0)
def colorize(text, foreground, background, attribute):
	"""Colorizes text."""
	return fg(foreground)+bg(background)+attr(attribute)+text+reset

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
				sub_dots = str(["?" if space["has_piece"] and space["is_hole"] and hard_mode else space["sub_dots"] for space in row])
				sub_dots = sub_dots.replace("False", "-")
				sub_dots = sub_dots.replace("'", "") #flush formatting
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
				DATA = DATA.replace("P5", colorize("P5", 124, 0, 4)) #red
				DATA = DATA.replace("P6", colorize("P6", 114, 0, 4)) #green
				DATA = DATA.replace("P7", colorize("P7", 104, 0, 4)) #blue
				DATA = DATA.replace("P8", colorize("P8", 94, 0, 4)) #yellow
				DATA = DATA.replace("C", colorize("C", 0, 7, 1)) #white bg
				DATA = DATA.replace("H", colorize("H", 0, 5, 1)) #purple bg
		else:
			for attribute in self.board_attributes:
				DATA += "{:^60}".format(attribute)
			DATA += "\n"
			for row in self.board:
				for attribute in self.board_attributes:
					DATA += "{:^60}".format(str([space[attribute] for space in row]))
				DATA += "\n"
		return DATA

	def __str__(self):
		"""__str__ method to print board data."""
		return self.board_output()

	def retrieve_attr_data(self):
		return (*[[[space[attribute] for space in row] for row in self.board] for attribute in self.board_attributes],)


class Actions(object):
	def __init__(self, board):
		"""Constructor for Actions class."""
		self.board = board

	def rotate(self, r):
		"""Rotate a board r rotations counterclockwise."""
		old_board = self.board #prevents self.board from being overwritten
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
		if center_name in CP_pieces: #"i33" is center
			piece = center_name
			piece_index = center_name
			print(CP_name, "has a piece in the center...")
		else:
			unblocked_pieces = [a_piece for a_piece in CP_pieces if len(self.legal_moves(self.find_correct_space(a_piece))) > 0]
			print("Available pieces:", CP_pieces)
			print("Unblocked_pieces:", unblocked_pieces)
			if len(unblocked_pieces) == 0:
				print(CP_name, "has no available pieces, all pieces are blocked")
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
			dots = self.board[int(piece_index[1])][int(piece_index[2])]["dots"]
			legal_spaces = self.legal_moves(piece_index)
			print(CP_name, "has a piece in the center...")
		else:
			while len(legal_spaces) == 0: #will not continue unless the selected piece has legal moves
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
					if hard_mode:
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
		self.players = {"P{}".format(n): {"pieces":[], "is_active": True} for n in range(1, self.player_count + 1)}

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
		"""Remove players when there are too many players for the number of starting spaces."""
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
		self.board_array = [B4, B3, B2, B1][[B4, B3, B2, B1].index(self.board):] #define board_array as list of boards being used
		self.player_count = player_count
		self.players = Players(self.player_count)
		self.random_gameplay = random_gameplay
		self.turn = 1
		self.winner = False

	def configure_boards(self):
		"""Rotate boards in board_array, add sub_dots."""
		for i in range(1, len(self.board_array)):
			r = random.randint(0,5)
			self.board_array[i] = Actions(self.board_array[i]).rotate(r) #rotate boards
			upper_board = self.board_array[i-1]
			lower_board = self.board_array[i]
			for x in range(len(upper_board)):
				for y in range(len(upper_board[x])):
					if upper_board[x][y]["is_hole"]:
						upper_board[x][y]["sub_dots"] = lower_board[x][y]["dots"]

	def get_starting_spaces(self):
		"""Get starting_spaces and cuts."""
		if self.board == B4:
			starting_spaces = [space["name"] for space in flatten(self.board) if space["starting_space"]]
			random.shuffle(starting_spaces)
			equal_spaces = (18//self.player_count)*self.player_count
			starting_spaces = starting_spaces[:equal_spaces]
		else:
			r = random.randint(0,5)
			upper_board = B2 if self.board == B1 else (B3 if self.board == B2 else B4)
			flat_upper_board = flatten(Actions(upper_board).rotate(r))
			flat_starting_board = flatten(self.board)
			starting_spaces = [item[0]["name"] for item in zip(flat_starting_board, flat_upper_board) if item[1]["is_hole"]]
			random.shuffle(starting_spaces)
		
		self.starting_spaces_length = len(starting_spaces)
		len_separations = min(self.player_count, self.starting_spaces_length)
		separations = [0]*len_separations
		for i in range(self.starting_spaces_length):
			separations[i%self.player_count] += 1
		random.shuffle(separations)

		return (starting_spaces, separations)

	def configure_players_random(self):
		"""Configure player object for random gameplay."""
		starting_spaces, pieces_per_player = self.get_starting_spaces()
		self.players.remove_inactive_players(self.starting_spaces_length)
		active_players = self.players.get_active_players()
		data = list(zip(active_players, pieces_per_player))
		player_names = flatten([[item[0]]*item[1] for item in data])
		assigned_pieces = list(zip(player_names, starting_spaces))
		for item in assigned_pieces:
			self.board[int(item[1][1])][int(item[1][2])]["has_piece"] = item[0]
		self.players.update_players(self.board)

	def configure_players(self):
		"""Configure player object for user-selected gameplay"""
		starting_spaces, pieces_per_player = self.get_starting_spaces()
		self.players.remove_inactive_players(self.starting_spaces_length)
		active_players = self.players.get_active_players()
		max_pieces = max(pieces_per_player)
		data = list(zip(active_players, pieces_per_player))
		player_order = flatten([[item[0] for item in data if n < item[1]] for n in range(max_pieces)])
		print("player order:", player_order) #order that players place pieces based on randomized pieces per player
		for name in player_order:
			print("Pick a space for", name)
			space_index = input("These are the remaining spaces... {}\n==> ".format(starting_spaces))
			while not space_index.isdigit() or int(space_index) >= self.starting_spaces_length:
				space_index = input("These are the remaining spaces... {}\n==> ".format(starting_spaces))
			selected_space = starting_spaces[int(space_index)]
			starting_spaces.remove(selected_space)
			x = int(selected_space[1]) #row
			y = int(selected_space[2]) #collumn
			self.board[x][y]["has_piece"] = name
			self.players.update_players(self.board)
			print(Display(self.board))

	def make_move(self):
		"""Make move for player."""
		center = self.board[3][3]
		if not center["has_piece"]:
			print("no piece in center")
			active_players = self.players.get_active_players()
			self.CP_name = "P1" if self.turn == 1 else active_players[(active_players.index(self.CP_name)+1)%len(active_players)] #checks index before assignment
		self.CP_pieces = self.players.players[self.CP_name]["pieces"] #fails if game starts with piece in center
		print(self.CP_name, "has these pieces:", self.CP_pieces)
		if len(self.CP_pieces) == 0:
			print(self.CP_name, "has no valid moves")
		else:
			if self.random_gameplay:
				Actions(self.board).take_turn_random(self.CP_pieces, self.CP_name)
			else:
				Actions(self.board).take_turn(self.CP_pieces, self.CP_name)

	def check_for_winner(self):
		"""Check for winner."""
		center = self.board[3][3]
		active_players = self.players.get_active_players()
		if len(self.board_array) == 1 and center["has_piece"]:
			self.winner = center["has_piece"]
		elif len(active_players) == 1:
			self.winner = active_players[0]
		return self.winner #default False unless reassigned here

	def imprint_board(self):
		"""Assigns pieces in holes to lower board."""
		next_board = self.board_array[1]
		for x in range(len(self.board)): #row
			for y in range(len(self.board[x])): #collumn
				if self.board[x][y]["has_piece"] and self.board[x][y]["is_hole"]:
					next_board[x][y]["has_piece"] = self.board[x][y]["has_piece"]
		self.board_array.pop(0)
		self.board = self.board_array[0] #self.board is now next board in self.board_array
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
			print("\n\n\nTURN NUMBER", self.turn)
			print(Display(self.board))
			self.players.update_players(self.board)
			self.make_move()

			center = self.board[3][3]
			if center["has_piece"]:
				print(Display(self.board))
				self.players.update_players(self.board)
				if self.check_for_winner():
					break
				self.make_move()

			#check if all pieces are in holes
			if all([space["has_piece"] for space in flatten(self.board) if space["is_hole"]]):
				print(Display(self.board))
				self.imprint_board()
				self.players.update_player_status(self.board)
				if self.check_for_winner():
					break

			self.turn += 1

		print("\n\nThere is a winner...")
		print(Display(self.board))
		print("\nTHE WINNER IS", self.winner)


def main():
	with open("out.txt", "w") as outfile:
		pass

	top_board = B3
	player_count = 2
	random_gameplay = True
	print_to_console = True

	if top_board not in [B4, B3, B2, B1]:
		raise ValueError("Only (B4, B3, B2, B1) are allowed")
	if player_count not in range(2, 19):
		raise ValueError("Valid input is int in range(2, 19)")
	if type(random_gameplay) != bool:
		raise ValueError("Valid input for random_gameplay is bool")

	Game = NewGame(top_board, player_count, random_gameplay)

	if print_to_console:
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
- supports more than four players
- allows you to choose a new move if you choose a move where all pieces are blocked
"""
