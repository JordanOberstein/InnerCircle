#Program by Jordan Oberstein
#Based on the the 1981 board game InnerCircle, (Milton Bradley company, board game originally designed by Virginia Charves)

import math
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
	def __init__(self, board, args=[]):
		""" 
		Constructor for Display class. 

		Parameters: 
			board: board to be displayed.
			args: (optional) specific arguments in board data to be displayed. 
		"""
		self.board = board
		self.args = args

	def board_output(self):
		"""Formats board data into readable output."""
		DATA = ""
		if len(self.args) == 0:
			DATA += "{:^120}".format("(name, has_piece, dots)")
			DATA += "{:^60}\n".format("sub_dots")
			for row in self.board:
				new_line = str([(space["name"], space["has_piece"], space["dots"]) for space in row])
				new_line = new_line.replace("False,", "--,") #has_piece
				new_line = new_line.replace("'", "") #flush formatting
				new_line = new_line.replace("), (", ") (") #flush formatting
				DATA += "{:^120}".format(new_line)
				sub_dots = str([(space["sub_dots"]) for space in row])
				sub_dots = sub_dots.replace("False", "-")
				DATA += "{:^60}\n".format(sub_dots)
			if colorize_board:
				DATA = DATA.replace("P1", colorize("P1", 1, 0, 4)) #red
				DATA = DATA.replace("P2", colorize("P2", 2, 0, 4)) #green
				DATA = DATA.replace("P3", colorize("P3", 4, 0, 4)) #blue
				DATA = DATA.replace("P4", colorize("P4", 3, 0, 4)) #yellow
				DATA = DATA.replace("C", colorize("C", 0, 7, 1)) #white bg
				DATA = DATA.replace("H", colorize("H", 0, 5, 1)) #purple bg
		else:
			for arg in self.args:
				DATA += "{:^60}".format(arg)
			DATA += "\n"
			for row in self.board:
				for arg in self.args:
					DATA += "{:^60}".format(str([space[arg] for space in row]))
				DATA += "\n"
		return DATA

	def __str__(self):
		"""__str__ method to print board data."""
		return Display(self.board, self.args).board_output()


class Setup(object):
	def __init__(self, board):
		"""Constructor for Setup class."""
		self.board = board

	def create_board(self, R1, R2, R3, center):
		"""Create board using rings."""
		eb = [[(), (), (), ()], \
		    [(), (), (), (), ()], \
		  [(), (), (), (), (), ()], \
		[(), (), (), (), (), (), ()], \
		  [(), (), (), (), (), ()], \
			[(), (), (), (), ()], \
			  [(), (), (), ()]]

		eb[2][2], eb[2][3], eb[3][4], eb[4][3], eb[4][2], eb[3][2] = R1[0], R1[1], R1[2], R1[3], R1[4], R1[5]
		eb[1][1], eb[1][2], eb[1][3], eb[2][4], eb[3][5], eb[4][4] = R2[0], R2[1], R2[2], R2[3], R2[4], R2[5]
		eb[5][3], eb[5][2], eb[5][1], eb[4][1], eb[3][1], eb[2][1] = R2[6], R2[7], R2[8], R2[9], R2[10], R2[11]
		eb[0][0], eb[0][1], eb[0][2], eb[0][3], eb[1][4], eb[2][5] = R3[0], R3[1], R3[2], R3[3], R3[4], R3[5]
		eb[3][6], eb[4][5], eb[5][4], eb[6][3], eb[6][2], eb[6][1] = R3[6], R3[7], R3[8], R3[9], R3[10], R3[11]
		eb[6][0], eb[5][0], eb[4][0], eb[3][0], eb[2][0], eb[1][0] = R3[12], R3[13], R3[14], R3[15], R3[16], R3[17]
		eb[3][3] = center
		return eb

	def rotate(self, r=1):
		"""Rotate a board counterclockwise, default 1 rotation."""
		new_board = self.board #prevents self.board from being written over by one sextant
		ring_1 = [new_board[2][2], new_board[2][3], new_board[3][4], new_board[4][3], new_board[4][2], new_board[3][2]]
		ring_2 = [new_board[1][1], new_board[1][2], new_board[1][3], new_board[2][4], new_board[3][5], new_board[4][4], \
			new_board[5][3], new_board[5][2], new_board[5][1], new_board[4][1], new_board[3][1], new_board[2][1]]
		ring_3 = [new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3], new_board[1][4], new_board[2][5], \
			new_board[3][6], new_board[4][5], new_board[5][4], new_board[6][3], new_board[6][2], new_board[6][1], \
			new_board[6][0], new_board[5][0], new_board[4][0], new_board[3][0], new_board[2][0], new_board[1][0]]
		
		#rotate each ring
		R1 = [ring_1[(n-(1*r))%len(ring_1)] for n in range(len(ring_1))]
		R2 = [ring_2[(n-(2*r))%len(ring_2)] for n in range(len(ring_2))]
		R3 = [ring_3[(n-(3*r))%len(ring_3)] for n in range(len(ring_3))]
		center = new_board[3][3]
		new_board = Setup(new_board).create_board(R1, R2, R3, center)
		return new_board

	def add_sub_dots(self, board_array):
		"""Add sub_dots to each board."""
		for b in range(0, len(board_array) - 1):
			top_board = board_array[b]
			bottom_board = board_array[b+1]
			for x in range(len(top_board)):
				for y in range(len(top_board[x])):
					if top_board[x][y]["is_hole"]:
						top_board[x][y]["sub_dots"] = bottom_board[x][y]["dots"]

	def add_pieces(self, active_players):
		"""Add pieces to top board."""
		turn = 1
		flat_board = [item for sublist in self.board for item in sublist] #flatten board
		player_count = len(active_players)
		while turn <= 16 if player_count == 4 else turn <= 18: #equal amount of starting pieces for each player
			print(Display(self.board))
			CP_name = active_players[turn%player_count - 1]
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			remaining_spaces = [space["name"] for space in flat_board if space["starting_space"] and not space["has_piece"]]
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
			turn += 1
		print(Display(self.board))
		print("Game Setup is complete.\n\n\n")

	def determine_starting_spaces(self):
		"""Determine starting spaces, used when not starting with top board."""
		if self.board == B1:
			r = random.randint(0,5)
			rotated_board_B2 = Setup(B2).rotate(r) #rotated upper board
			flat_rotated_board_B2 = [item for sublist in rotated_board_B2 for item in sublist] #flatten rotated upper board
			flat_board_B1 = [item for sublist in B1 for item in sublist] #flatten lower board
			starting_index_list = [flat_rotated_board_B2.index(item) for item in flat_rotated_board_B2 if item["is_hole"]] 
			return [flat_board_B1[n]["name"] for n in starting_index_list] #spaces in lower board that align with holes in upper board
		elif self.board == B2:
			r = random.randint(0,5)
			rotated_board_B3 = Setup(B3).rotate(r) #rotated upper board
			flat_rotated_board_B3 = [item for sublist in rotated_board_B3 for item in sublist] #flatten rotated upper board
			flat_board_B2 = [item for sublist in B2 for item in sublist] #flatten lower board
			starting_index_list = [flat_rotated_board_B3.index(item) for item in flat_rotated_board_B3 if item["is_hole"]] 
			return [flat_board_B2[n]["name"] for n in starting_index_list] #spaces in lower board that align with holes in upper board
		elif self.board == B3:
			r = random.randint(0,5)
			rotated_board_B4 = Setup(B4).rotate(r) #rotated upper board
			flat_rotated_board_B4 = [item for sublist in rotated_board_B4 for item in sublist] #flatten rotated upper board
			flat_board_B3 = [item for sublist in B3 for item in sublist] #flatten lower board
			starting_index_list = [flat_rotated_board_B4.index(item) for item in flat_rotated_board_B4 if item["is_hole"]] 
			return [flat_board_B3[n]["name"] for n in starting_index_list] #spaces in lower board that align with holes in upper board
		else:
			raise ValueError("Only (B1, B2, B3) are allowed")

	def check_for_complete_board(self):
		"""Check if a piece occupies all holes on a board."""
		flat_board = [item for sublist in self.board for item in sublist] #flatten board
		return (all([space["has_piece"] for space in flat_board if space["is_hole"]])) #if all holes have a piece

	def imprint_board(self, new_board):
		"""Assigns pieces in holes to lower board."""
		for x in range(len(self.board)): #row
			for y in range(len(self.board[x])): #collumn
				if self.board[x][y]["has_piece"] and self.board[x][y]["is_hole"]:
					new_board[x][y]["has_piece"] = self.board[x][y]["has_piece"]


class Actions(object):
	def __init__(self, board):
		"""Constructor for Actions class."""
		self.board = board

	def find_correct_space(self, piece):
		"""Determines correct space based on name of piece."""
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		for a in range(len(self.board)):
			for b in range(len(self.board[a])):
				if self.board[a][b]["name"] == "i{}{}".format(x, y):
					return "i{}{}".format(a, b)

	def legal_moves(self, piece=False):
		"""Determines legal moves for a given piece."""
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		dots = self.board[x][y]["dots"]
		print("Piece {} moves {} spaces".format(piece, dots))
		legal_spaces = [space for space in self.board[x][y]["moves_to"]]
		legal_spaces_without_pieces = [] 
		for space in legal_spaces: #determine legal spaces based on the pieces surrounding the index of the chosen move
			piece_index_x = int(Actions(self.board).find_correct_space(space)[1])
			piece_index_y = int(Actions(self.board).find_correct_space(space)[2])
			if not self.board[piece_index_x][piece_index_y]["has_piece"]:
				legal_spaces_without_pieces.append(space)
		return legal_spaces_without_pieces

	def take_turn(self, CP, CP_name):
		"""Execute turn for current player."""
		center = "i33"
		legal_spaces = []
		available_pieces = CP.copy()

		if center in CP:
			piece = center
			piece_index = center
			legal_spaces = [space for space in Actions(self.board).legal_moves(piece) if space != False]
		else:
			while len(legal_spaces) == 0: #will not continue unless the chosen piece has legal moves
				print("Checking for moves...")
				if len(available_pieces) == 0:
					print("{} has no available pieces, all pieces are blocked".format(CP_name))
					return False
				print("Available pieces: {}".format(str(available_pieces)))
				
				if random_gameplay:
					piece_index = random.randint(0, len(available_pieces) - 1)
				else:
					piece_index = input("These are the available pieces (not already in holes) for {}, choose 1: {}:\n==> ".format(CP_name, available_pieces))
					while not piece_index.isdigit() or int(piece_index) >= len(available_pieces):
						piece_index = input("These are the available pieces (not already in holes) for {}, choose 1: {}:\n==> ".format(CP_name, available_pieces))

				piece = available_pieces[int(piece_index)]
				print("Selected piece from list is piece {}".format(piece))
				piece_index = Actions(self.board).find_correct_space(piece)
				print("Selected piece rotates into index {}".format(piece_index))

				legal_spaces = [space for space in Actions(self.board).legal_moves(piece_index)] #determines legal spaces
				available_pieces.remove(piece)

		print("Legal spaces: {}".format(str(legal_spaces)))

		if random_gameplay:
			legal_spaces_index = random.randint(0, len(legal_spaces) - 1)
		else:
			legal_spaces_index = input("These are the available moves for piece {}, choose 1: {}:\n==> ".format(piece, legal_spaces))
			while not legal_spaces_index.isdigit() or int(legal_spaces_index) >= len(legal_spaces):
				legal_spaces_index = input("These are the available moves for piece {}, choose 1: {}:\n==> ".format(piece, legal_spaces))

		selected_move = legal_spaces[int(legal_spaces_index)]

		x0 = int(piece_index[1]) #row index
		y0 = int(piece_index[2]) #collumn index
		print("Selected piece's index is: ({}, {})".format(x0, y0))

		x1 = int(selected_move[1]) #new row
		y1 = int(selected_move[2]) #new collumn
		print("Selected move from list is: ({}, {})".format(x1, y1))

		selected_move_index = Actions(self.board).find_correct_space(selected_move)
		x1 = int(selected_move_index[1]) #new row index
		y1 = int(selected_move_index[2]) #new collumn index
		print("Selected move's index is: ({}, {})".format(x1, y1))

		#make move on board
		self.board[x0][y0]["has_piece"] = False
		self.board[x1][y1]["has_piece"] = CP_name

		CP.remove(piece)
		CP.append(selected_move)


class FullGame(object):
	def __init__(self, board, player_count):
		""" 
		Constructor for FullGame class. 

		Parameters: 
			board: the top board for gameplay (B1, B2, B3, B4). 
			player_count: the number of players playing the game (2, 3, 4). 
		"""
		self.board = board
		self.player_count = player_count
		if self.player_count not in range(2, 5):
			raise ValueError("Only (2, 3, 4) are valid player number inputs")

		#self.players = {"P{}".format(n): {"pieces":[], "is_active": True if player_count > n-1 else False} for n in range(1, 5)}
		self.players = {
			"P1": {
				"pieces": [],
				"is_active": True
			},
			"P2": {
				"pieces": [],
				"is_active": True
			},
			"P3": {
				"pieces": [],
				"is_active": True if self.player_count > 2 else False
			},
			"P4": {
				"pieces": [],
				"is_active": True if self.player_count > 3 else False
			}
		}
		self.turn = 1

		board_array = [B4, B3, B2, B1]
		if self.board not in board_array:
			raise ValueError("Only (B1, B2, B3, B4) are allowed")
		self.board_array = board_array[board_array.index(self.board):] #redefine board_array as only boards being used


	def play(self):
		"""Play a complete game."""
		for b in range(1, len(self.board_array)):
			r = random.randint(0,5)
			self.board_array[b] = Setup(self.board_array[b]).rotate(r) #rotate boards

		Setup(self.board).add_sub_dots(self.board_array)

		if self.board == B4:
			active_players = [player for player in self.players if self.players[player]["is_active"]]
			Setup(self.board).add_pieces(active_players)
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			for player in active_players:
				self.players[player]["pieces"] = [space["name"] for space in flat_board if space["has_piece"] == player and not space["is_hole"]]
		else:
			starting_spaces = Setup(self.board).determine_starting_spaces() #len = 3, 7, 10
			random.shuffle(starting_spaces) #shuffle the starting spaces, otherwise cut for P1 and P2 will be the same for some given rotation
			if self.player_count == 2:
				cut = random.randint(math.floor(len(starting_spaces)/2), math.ceil(len(starting_spaces)/2)) #cut in half, assumes players play decently
				self.players["P1"]["pieces"] = starting_spaces[:cut]
				self.players["P2"]["pieces"] = starting_spaces[cut:]
			elif self.player_count == 3:
				if self.board == B1:
					cut1, cut2 = 1, 2
				elif self.board == B2:
					(cut1, cut2) = random.choice([(3, 5), (2, 5), (2, 4)])
				elif self.board == B3:
					(cut1, cut2) = random.choice([(4, 7), (3, 7), (3, 6)])
				self.players["P1"]["pieces"] = starting_spaces[:cut1]
				self.players["P2"]["pieces"] = starting_spaces[cut1:cut2]
				self.players["P3"]["pieces"] = starting_spaces[cut2:]
			elif self.player_count == 4:
				if self.board == B1:
					cut1, cut2 = 1, 2
					self.players["P1"]["pieces"] = starting_spaces[:cut1]
					self.players["P2"]["pieces"] = starting_spaces[cut1:cut2]
					self.players["P3"]["pieces"] = starting_spaces[cut2:]
					self.players["P4"]["is_active"] = False #four players cannot occupy three spaces
				else:
					if self.board == B2:
						(cut1, cut2, cut3) = random.choice([(2, 4, 6), (2, 4, 5), (2, 3, 5), (1, 3, 5)])
					elif self.board == B3:
						(cut1, cut2, cut3) = random.choice([(3, 6, 8), (3, 5, 8), (3, 5, 7), (2, 5, 8), (2, 5, 7), (2, 4, 7)])
					self.players["P1"]["pieces"] = starting_spaces[:cut1]
					self.players["P2"]["pieces"] = starting_spaces[cut1:cut2]
					self.players["P3"]["pieces"] = starting_spaces[cut2:cut3]
					self.players["P4"]["pieces"] = starting_spaces[cut3:]
			#add pieces to the board
			active_players = [player for player in self.players if self.players[player]["is_active"]]
			for player in active_players:
				print(player, self.players[player]["pieces"])
				for space in self.players[player]["pieces"]:
					self.board[int(space[1])][int(space[2])]["has_piece"] = player #x=space[1], y=space[2]

		winner = ""
		continue_game = True
		while continue_game:
			print("\n\n\nMOVE NUMBER {}".format(self.turn))
			print(Display(self.board))

			#update player object to only pieces that are not in holes
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			active_players = [player for player in self.players if self.players[player]["is_active"]]
			for player in active_players:
				self.players[player]["pieces"] = [space["name"] for space in flat_board if space["has_piece"] == player and not space["is_hole"]]
			
			#determine current player
			if self.turn == 1:
				CP_name = "P1"
			else:
				old_index = active_players.index(CP_name)
				CP_name = active_players[(old_index+1)%len(active_players)]
			CP = self.players[CP_name]["pieces"]
			print(CP, CP_name)

			#if current player has no legal moves
			if len(CP) == 0:
				print("No valid moves for {}".format(CP_name))
				self.turn += 1
				continue

			Actions(self.board).take_turn(CP, CP_name)

			#check if piece is in center, end game if on lowest board
			center = self.board[3][3] #redefine center to update when moving down boards
			if center["has_piece"]:
				if len(self.board_array) == 1:
					winner = center["has_piece"]
					break
				else:
					print("\n{}'s piece is in the center, they will now move it...\n".format(CP_name))
					print(Display(self.board))
					Actions(self.board).take_turn(CP, CP_name) #take_turn will only allow piece in center to move

			#check if all pieces are in holes
			if Setup(self.board).check_for_complete_board():
				print(Display(self.board))
				Setup(self.board).imprint_board(self.board_array[1])
				self.board_array.pop(0)
				self.board = self.board_array[0] #self.board is next board in self.board_array
				print("\n\n\nALL SPACES ON BOARD B{} ARE FILLED, MOVING DOWN TO BOARD B{}\n\n\n".format(len(self.board_array)+1, len(self.board_array)))

				#update player object after imprinting board
				flat_board = [item for sublist in self.board for item in sublist] #flatten board
				active_players = [player for player in self.players if self.players[player]["is_active"]]
				for player in active_players:
					self.players[player]["pieces"] = [space["name"] for space in flat_board if space["has_piece"] == player]
					if len(self.players[player]["pieces"]) == 0:
						self.players[player]["is_active"] = False

				#check for winner
				active_players = [player for player in self.players if self.players[player]["is_active"]]
				if len(active_players) == 1:
					winner = active_players[0]
					break

			self.turn += 1

		print("\n\nThere is a winner...")
		print(Display(self.board))
		print("\n\nTHE WINNER IS: {}".format(winner))


def main():
	if print_to_console:
		FullGame(B2, 4).play()
	else:
		with HiddenPrints():
			FullGame(B2, 4).play()
		

if __name__ == "__main__":
	main()


"""
Conversion to multiplayer

use proper reset method to loop through multiple games


TO-DO:
Expand and clarify docstrings

IDEAS:
Add support for 3 and 4 player games
Create GUI
Create move trees and determine winning strategy
Create AI to learn game, find optimal strategy

Determine which starting space has the highest winning percentage via using 18 player
"""
