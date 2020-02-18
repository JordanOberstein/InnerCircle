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
		R1 = [ring_1[(n-(1*r))%len(ring_1)] for n in range(len(ring_1))]
		R2 = [ring_2[(n-(2*r))%len(ring_2)] for n in range(len(ring_2))]
		R3 = [ring_3[(n-(3*r))%len(ring_3)] for n in range(len(ring_3))]
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

	def add_sub_dots(self, board_array):
		"""Add sub_dots to each board."""
		for i in range(0, len(board_array) - 1):
			top_board = board_array[i]
			bottom_board = board_array[i+1]
			for x in range(len(top_board)):
				for y in range(len(top_board[x])):
					if top_board[x][y]["is_hole"]:
						top_board[x][y]["sub_dots"] = bottom_board[x][y]["dots"]

	def add_pieces(self, active_players):
		"""Add pieces to top board."""
		turn = 1
		player_count = len(active_players)
		max_turns = (math.ceil(19/player_count)-1)*player_count
		while turn <= max_turns: #equal number of starting pieces for each player
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
			turn += 1
		print(Display(self.board))
		print("Game Setup is complete.\n\n\n")

	def determine_starting_spaces(self):
		"""Determine starting spaces, used when not starting with top board."""
		if self.board == B1:
			r = random.randint(0,5)
			B2_rotated = Setup(B2).rotate(r) #randomly rotated upper board
			B2_rotated_flattened = flatten(B2_rotated)
			B1_flattened = flatten(B1)
			return [B1_flattened[n]["name"] for n in range(len(B1_flattened)) if B2_rotated_flattened[n]["is_hole"]] #spaces in lower board that align with holes in upper board
		elif self.board == B2:
			r = random.randint(0,5)
			B3_rotated = Setup(B3).rotate(r) #randomly rotated upper board
			B3_rotated_flattened = flatten(B3_rotated)
			B2_flattened = flatten(B2)
			return [B2_flattened[n]["name"] for n in range(len(B2_flattened)) if B3_rotated_flattened[n]["is_hole"]] #spaces in lower board that align with holes in upper board
		elif self.board == B3:
			r = random.randint(0,5)
			B4_rotated = Setup(B4).rotate(r) #randomly rotated upper board
			B4_rotated_flattened = flatten(B4_rotated)
			B3_flattened = flatten(B3)
			return [B3_flattened[n]["name"] for n in range(len(B3_flattened)) if B4_rotated_flattened[n]["is_hole"]] #spaces in lower board that align with holes in upper board
		else:
			raise ValueError("Only (B1, B2, B3) are allowed")

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

	def legal_moves(self, piece):
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
				if hard_mode and len(legal_spaces) == 0:
					print("Selected piece is blocked.")
					return False

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
			player_count: the number of players playing the game int in range(2, 19). 
		"""
		self.board = board
		self.player_count = player_count
		if self.player_count not in range(2, 19):
			raise ValueError("Only int in range(2, 19) are valid player number inputs")
		self.players = {"P{}".format(n): {"pieces":[], "is_active": True} for n in range(1, self.player_count + 1)}
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

		#add pieces to board and pieces to each player in player object
		if self.board == B4:
			active_players = [player for player in self.players if self.players[player]["is_active"]]
			Setup(self.board).add_pieces(active_players)
			for player in active_players:
				self.players[player]["pieces"] = [space["name"] for space in flatten(self.board) if space["has_piece"] == player and not space["is_hole"]]
		else:
			starting_spaces = Setup(self.board).determine_starting_spaces()
			random.shuffle(starting_spaces)
			separations = [0]*self.player_count
			for i in range(len(starting_spaces)):
				separations[i%self.player_count] += 1
			separations = [num for num in separations if num != 0]
			random.shuffle(separations)
			cuts = [0] + [sum(separations[:y]) for y in range(1, len(separations) + 1)]

			#remove players who are eliminated due to not having enough spaces
			if self.player_count > len(starting_spaces):
				for player in self.players:
					if int(player[1:]) > len(starting_spaces):
						self.players[player]["is_active"] = False

			active_players = [player for player in self.players if self.players[player]["is_active"]]
			for n in range(len(active_players)):
				player = active_players[n]
				self.players[player]["pieces"] = starting_spaces[cuts[n]:cuts[n+1]]
				print(player, self.players[player]["pieces"])
				for space in self.players[player]["pieces"]:
					self.board[int(space[1])][int(space[2])]["has_piece"] = player

		winner = ""
		continue_game = True
		while continue_game:
			print("\n\n\nTURN NUMBER {}".format(self.turn))
			print(Display(self.board))

			#update player object to only pieces that are not in holes
			active_players = [player for player in self.players if self.players[player]["is_active"]]
			for player in active_players:
				self.players[player]["pieces"] = [space["name"] for space in flatten(self.board) if space["has_piece"] == player and not space["is_hole"]]
			
			#determine current player
			CP_name = "P1" if self.turn == 1 else active_players[(active_players.index(CP_name)+1)%len(active_players)] #checks index before assignment
			CP = self.players[CP_name]["pieces"]
			print(CP_name, CP)

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
			if all([space["has_piece"] for space in flatten(self.board) if space["is_hole"]]):
				print(Display(self.board))
				Setup(self.board).imprint_board(self.board_array[1])
				self.board_array.pop(0)
				self.board = self.board_array[0] #self.board is next board in self.board_array
				print("\n\n\nALL SPACES ON BOARD B{} ARE FILLED, MOVING DOWN TO BOARD B{}\n\n\n".format(len(self.board_array)+1, len(self.board_array)))

				#update player object after imprinting board
				active_players = [player for player in self.players if self.players[player]["is_active"]]
				for player in active_players:
					self.players[player]["pieces"] = [space["name"] for space in flatten(self.board) if space["has_piece"] == player]
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
		FullGame(B4, 2).play()
	else:
		with HiddenPrints():
			FullGame(B4, 2).play()
		

if __name__ == "__main__":
	main()


"""
TO-DO:
Expand and clarify docstrings
Add proper reset method instead of using loop in seperate file to execute file multiple times

IDEAS:
Add support for 3 and 4 player games
Create GUI
Create move trees and determine winning strategy
Create AI to learn game, find optimal strategy

Determine which starting space has the highest winning percentage via using 18 player

DIFFERENCES FROM MAIN GAME:
- supports more than four players
- allows you to choose a new move if you choose a move where all pieces are blocked
"""
