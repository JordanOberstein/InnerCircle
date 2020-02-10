#Program by Jordan Oberstein
#Based on the the 1981 board game InnerCircle, (Milton Bradley company, originally designed by Virginia Charves)

import math
import random
from colored import fg, bg, attr

from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4


colorize_board = False
random_gameplay = True

def colorize(text, foreground, background, attribute):
	"""Colorizes text."""
	return "{}{}{}{}".format(fg(foreground), bg(background), attr(attribute), text) + "{}{}{}".format(fg(15), bg(0), attr(0))


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
			for row in self.board: #board rows
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
				DATA = DATA.replace("C", colorize("C", 3, 0, 1)) #yellow
				DATA = DATA.replace("H", colorize("H", 4, 0, 1)) #blue
		else:
			for arg in self.args: #name of arg
				DATA += "{:^60}".format(arg)
			DATA += "\n"
			for row in self.board: #board rows
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
		empty_board = [[(), (), (), ()], \
					[(), (), (), (), ()], \
				  [(), (), (), (), (), ()], \
				[(), (), (), (), (), (), ()], \
				  [(), (), (), (), (), ()], \
					[(), (), (), (), ()], \
					  [(), (), (), ()]]

		nb = empty_board
		nb[2][2], nb[2][3], nb[3][4], nb[4][3], nb[4][2], nb[3][2] = R1[0], R1[1], R1[2], R1[3], R1[4], R1[5]
		nb[1][1], nb[1][2], nb[1][3], nb[2][4], nb[3][5], nb[4][4] = R2[0], R2[1], R2[2], R2[3], R2[4], R2[5]
		nb[5][3], nb[5][2], nb[5][1], nb[4][1], nb[3][1], nb[2][1] = R2[6], R2[7], R2[8], R2[9], R2[10], R2[11]
		nb[0][0], nb[0][1], nb[0][2], nb[0][3], nb[1][4], nb[2][5] = R3[0], R3[1], R3[2], R3[3], R3[4], R3[5]
		nb[3][6], nb[4][5], nb[5][4], nb[6][3], nb[6][2], nb[6][1] = R3[6], R3[7], R3[8], R3[9], R3[10], R3[11]
		nb[6][0], nb[5][0], nb[4][0], nb[3][0], nb[2][0], nb[1][0] = R3[12], R3[13], R3[14], R3[15], R3[16], R3[17]
		nb[3][3] = center
		return nb

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

	def add_pieces(self):
		"""Add pieces to top board."""
		players = ["P2", "P1"] #P1 is odd indices, P2 is even indices
		turn = 1
		flat_board = [item for sublist in self.board for item in sublist] #flatten board
		while not all([space["has_piece"] for space in flat_board if space["starting_space"]]): #if all starting spaces have a piece
			print(Display(self.board))
			CP = players[turn%2]
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
			self.board[x][y]["has_piece"] = CP
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
			print("Not a valid board for starting spaces.")
			return False

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
	def __init__(self, board):
		""" 
		Constructor for FullGame class. 

		Parameters: 
			board: the top board for gameplay (B1, B2, B3, B4). 
		"""
		self.board = board
		self.P1 = []
		self.P2 = []
		self.players = [self.P2, self.P1] #P1 is odd indices, P2 is even indices
		self.turn = 1

	def play(self):
		"""Play a complete game."""
		board_array = [B4, B3, B2, B1]
		board_array = board_array[board_array.index(self.board):] #define board_array as only boards being used

		for b in range(1, len(board_array)):
			r = random.randint(0,5)
			board_array[b] = Setup(board_array[b]).rotate(r) #rotate boards

		Setup(self.board).add_sub_dots(board_array)

		if self.board == B4:
			Setup(B4).add_pieces()
			#retrieve P1 and P2 after adding pieces to board
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1"]
			self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2"]
		elif self.board == B1 or self.board == B2 or self.board == B3:
			starting_spaces = Setup(self.board).determine_starting_spaces()
			random.shuffle(starting_spaces) #shuffle the starting spaces, otherwise cut for P1 and P2 will be the same for some given rotation
			cut = random.randint(math.floor(len(starting_spaces)/2), math.ceil(len(starting_spaces)/2)) #cut in half, assumes players play decently
			self.P1 = starting_spaces[:cut].copy()
			self.P2 = starting_spaces[cut:].copy()
			#add pieces in P1 and P2 to the board
			for space in self.P1:
				self.board[int(space[1])][int(space[2])]["has_piece"] = "P1" #x=space[1], y=space[2]
			for space in self.P2:
				self.board[int(space[1])][int(space[2])]["has_piece"] = "P2" #x=space[1], y=space[2]

		winner = ""
		continue_game = True
		while continue_game:
			print("\n\n\nMOVE NUMBER {}".format(self.turn))
			print(Display(self.board))

			#redefine self.P1 and self.P2 to include only pieces that are not in holes
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1" and not space["is_hole"]]
			self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2" and not space["is_hole"]]
			self.players = [self.P2, self.P1]
			CP = self.players[self.turn%2]
			CP_name = "P" + str(((self.turn + 1)%2)+1)
			
			#if current player has no legal moves
			if len(CP) == 0:
				print("No valid moves for {}".format(CP_name))
				self.turn += 1
				continue

			Actions(self.board).take_turn(CP, CP_name)

			#check if piece is in center, end game if on lowest board
			center = self.board[3][3] #redefine center to update when moving down baords
			if center["has_piece"]:
				if len(board_array) == 1:
					winner = center["has_piece"]
					break
				else:
					print("\n{}'s piece is in the center, they will now move it...\n".format(CP_name))
					print(Display(self.board))
					Actions(self.board).take_turn(CP, CP_name) #take_turn will only allow piece in center to move

			#check if all pieces are in holes
			if Setup(self.board).check_for_complete_board():
				print(Display(self.board))
				Setup(self.board).imprint_board(board_array[1])
				board_array.pop(0)
				self.board = board_array[0] #self.board is next board in board_array

				print("\n\n\nALL SPACES ON BOARD B{} ARE FILLED, MOVING DOWN TO BOARD B{}\n\n\n".format(len(board_array)+1, len(board_array)))

				#check if both players still have pieces
				flat_board = [item for sublist in self.board for item in sublist] #flatten board
				self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1"]
				self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2"]
				if len(self.P1) == 0:
					winner = "P2"
					break
				if len(self.P2) == 0:
					winner = "P1"
					break

			self.turn += 1


		print("\n\nThere is a winner...")
		print(Display(self.board))
		print("\n\nTHE WINNER IS: {}".format(winner))


def main():
	outfile = open("out.txt", "w")
	outfile.close()
	FullGame(B4).play()

if __name__ == "__main__":
	main()


"""
TO-DO:
Expand and clarify docstrings

IDEAS:
Add support for 3 and 4 player games
Create GUI
Create move trees and determine winning strategy
Create AI to learn game, find optimal strategy
"""