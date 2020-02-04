#Code by Jordan Oberstein
#Based on the the 1981 board game InnerCircle, (Milton Bradley company, originally designed by Virginia Charves)

import math
import random
from colored import fg, bg, attr

from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4

#currently uneeded
#from board1 import B1_Data
#from board2 import B2_Data
#from board3 import B3_Data
#from board4 import B4_Data

colorize_board = True


def colorize(text, foreground, background, attribute):
	return '{}{}{}{}'.format(fg(foreground), bg(background), attr(attribute), text) + '{}{}{}'.format(fg(15), bg(0), attr(0))

class Display(object):
	def __init__(self, board, args=[]):
		self.board = board
		self.args = args

	def __str__(self):
		DATA = ""
		if len(self.args) == 0:
			args = ["name", "has_piece", "dots"]
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

		elif self.args == ["adj"]: #checking if all directions in adj are correct CURRENTLY UNUSED
			directions = ["ul", "ur", "r", "br", "bl", "l"]
			for d in directions:
				DATA += "{:^60}\n".format(d)
				for row in self.board:
					DATA += "{:^60}".format(str([space["adj"][d] for space in row]))
					DATA += "{:^60}\n".format(str([space["name"] for space in row]))
		else:
			for arg in self.args: #name of arg
				DATA += "{:^60}".format(arg)
			DATA += "\n"
			for row in self.board: #board rows
				for arg in self.args:
					DATA += "{:^60}".format(str([space[arg] for space in row]))
				DATA += "\n"
		return DATA


class Setup(object):
	def __init__(self, board): #should only be B4
		self.board = board

	def create_board(self, R1, R2, R3, center): #create board using rings
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

	def rotate(self, r=1): #default 1 rotation clockwise
		new_board = self.board #prevents glitches where whole board is written over with one sextant
		ring_1 = [new_board[2][2], new_board[2][3], new_board[3][4], new_board[4][3], new_board[4][2], new_board[3][2]]
		ring_2 = [new_board[1][1], new_board[1][2], new_board[1][3], new_board[2][4], new_board[3][5], new_board[4][4], \
			new_board[5][3], new_board[5][2], new_board[5][1], new_board[4][1], new_board[3][1], new_board[2][1]]
		ring_3 = [new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3], new_board[1][4], new_board[2][5], \
			new_board[3][6], new_board[4][5], new_board[5][4], new_board[6][3], new_board[6][2], new_board[6][1], \
			new_board[6][0], new_board[5][0], new_board[4][0], new_board[3][0], new_board[2][0], new_board[1][0]]
		#rotate rings
		R1 = [ring_1[(n-(1*r))%len(ring_1)] for n in range(len(ring_1))] #n-(1*r)
		R2 = [ring_2[(n-(2*r))%len(ring_2)] for n in range(len(ring_2))] #n-(2*r)
		R3 = [ring_3[(n-(3*r))%len(ring_3)] for n in range(len(ring_3))] #n-(3*r)
		center = new_board[3][3]
		new_board = Setup(new_board).create_board(R1, R2, R3, center)
		return new_board

	def add_pieces(self):
		players = ["P2", "P1"] #index 0, 2, 4 is P2, index 1, 3, 5 is P1
		turn = 1
		flat_board = [item for sublist in self.board for item in sublist] #flatten board
		while not all([space["has_piece"] for space in flat_board if space["starting_space"]]): #if all starting spaces have a piece
			CP = players[turn%2]
			print(Display(self.board))
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			remaining_spaces = [space["name"] for space in flat_board if space["starting_space"] and not space["has_piece"]]
			space_index = input("These are the remaining spaces, choose 1: {}\n==> ".format(remaining_spaces))
			chosen_space = remaining_spaces[int(space_index)]
			x = int(chosen_space[1]) #row
			y = int(chosen_space[2]) #collumn
			self.board[x][y]["has_piece"] = CP
			turn += 1
		print(Display(self.board))
		print("Game Setup is complete.\n\n\n")

	def determine_starting_spaces(self): #for incomplete games 
		if self.board == B1: #playing with just first board
			r = random.randint(0,5)
			rotated_board_B2 = Setup(B2).rotate(r) #rotated upper board
			flat_rotated_board_B2 = [item for sublist in rotated_board_B2 for item in sublist] #flatten rotated upper board
			flat_board_B1 = [item for sublist in B1 for item in sublist] #flatten lower board
			#list of indexes of spaces in upper board where spaces are holes
			starting_index_list = [flat_rotated_board_B2.index(item) for item in flat_rotated_board_B2 if item["is_hole"]] 
			return [flat_board_B1[n]["name"] for n in starting_index_list] #spaces in lower board that line up with holes in upper board
		elif self.board == B2: #playing with first and second board
			r = random.randint(0,5)
			rotated_board_B3 = Setup(B3).rotate(r) #rotated upper board
			flat_rotated_board_B3 = [item for sublist in rotated_board_B3 for item in sublist] #flatten rotated upper board
			flat_board_B2 = [item for sublist in B2 for item in sublist] #flatten lower board
			#list of indexes of spaces in upper board where spaces are holes
			starting_index_list = [flat_rotated_board_B3.index(item) for item in flat_rotated_board_B3 if item["is_hole"]] 
			return [flat_board_B2[n]["name"] for n in starting_index_list] #spaces in lower board that line up with holes in upper board
		elif self.board == B3: #playing with first, second, and third board
			r = random.randint(0,5)
			rotated_board_B4 = Setup(B4).rotate(r) #rotated upper board
			flat_rotated_board_B4 = [item for sublist in rotated_board_B4 for item in sublist] #flatten rotated upper board
			flat_board_B3 = [item for sublist in B3 for item in sublist] #flatten lower board
			#list of indexes of spaces in upper board where spaces are holes
			starting_index_list = [flat_rotated_board_B4.index(item) for item in flat_rotated_board_B4 if item["is_hole"]] 
			return [flat_board_B3[n]["name"] for n in starting_index_list] #spaces in lower board that line up with holes in upper board
		else:
			print("Not a valid board for starting spaces.")
			return False

	def check_for_complete_board(self):
		flat_board = [item for sublist in self.board for item in sublist] #flatten board
		return (all([space["has_piece"] for space in flat_board if space["dots"] == "H"])) #if all holes have a piece

	def imprint_board(self, new_board):
		for x in range(len(self.board)): #row
			for y in range(len(self.board[x])): #collumn
				if self.board[x][y]["has_piece"] and self.board[x][y]["is_hole"]: #if self.board has a piece and the space is a hole 
					new_board[x][y]["has_piece"] = self.board[x][y]["has_piece"]

	def add_sub_dots(self, board_array):
		for b in range(0, len(board_array) - 1):
			top_board = board_array[b]
			bottom_board = board_array[b+1]
			for x in range(len(top_board)):
				for y in range(len(top_board[x])):
					if top_board[x][y]["is_hole"]:
						top_board[x][y]["sub_dots"] = bottom_board[x][y]["dots"] #retrieve dots from lower layer


#this is a seperate class from gameplay because gameplay must initialize ONLY once, otherwise random choices get reset
class Actions(object):
	def __init__(self, board):
		self.board = board

	def legal_moves(self, piece=False):
		if not piece:
			return "no piece, add argument in legal_moves"
		
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		dots = self.board[x][y]["dots"] #number of dots

		print("Piece {} moves {} spaces".format(piece, dots))

		#all legal spaces not already containing a piece
		legal_spaces = [space for space in self.board[x][y]["moves_to"]]
		legal_spaces_without_pieces = [space for space in legal_spaces if not self.board[int(space[1])][int(space[2])]["has_piece"]]
		
		return legal_spaces_without_pieces

	def take_turn(self, turn, CP):
		CP_name = "P" + str(((turn + 1)%2)+1)
		legal_spaces = []
		center = "i33"

		available_pieces = CP.copy() #if a piece is chosen and is completely blocked, it can remove it from this copy of CP

		if center in CP:
			piece = center
			legal_spaces = [space for space in Actions(self.board).legal_moves(piece) if space != False]
		else:
			while len(legal_spaces) == 0: #will not continue unless the chosen piece has legal moves
				if len(available_pieces) == 0:
					print("{} has no available pieces, all pieces are blocked".format(CP_name))
					return False
				piece_index = input("These are the available pieces (not already in holes) for {}, choose 1: {}:\n==> ".format(CP_name, available_pieces)) #"P2" if turn % 2 == 0 else "P1"
				piece = available_pieces[int(piece_index)]
				legal_spaces = [space for space in Actions(self.board).legal_moves(piece)] #determines legal spaces
				available_pieces.remove(piece)

		move_index = input("These are the available moves for piece {}, choose 1: {}:\n==> ".format(piece, legal_spaces))
		chosen_move = legal_spaces[int(move_index)]

		#now make the move
		x0 = int(piece[1]) #row
		y0 = int(piece[2]) #collumn
		x1 = int(chosen_move[1]) #new row
		y1 = int(chosen_move[2]) #new collumn

		self.board[x0][y0]["has_piece"] = False
		self.board[x1][y1]["has_piece"] = CP_name
		CP.remove(piece)
		CP.append(chosen_move)


class FullGame(object):
	def __init__(self, board):
		self.board = board
		self.P1 = []
		self.P2 = []
		self.players = [self.P1, self.P2] #index 0, 2, 4 is P2, index 1, 3, 5 is P1
		self.turn = 1 #moves in game; move from P1 + move from P2 = 1 turn
		self.center = self.board[3][3]

	def play(self):
		board_array = [B4, B3, B2, B1]

		#Add pieces to board at start of game
		if self.board == B4:
			#rotate boards
			for b in range(1, len(board_array)):
				r = random.randint(0,5)
				board_array[b] = Setup(board_array[b]).rotate(r)

			Setup(self.board).add_sub_dots(board_array)
			Setup(B4).add_pieces()
			
			#retrieve P1 and P2
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1"]
			self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2"]
		
		elif self.board == B1 or self.board == B2 or self.board == B3:
			board_array = board_array[board_array.index(self.board):] #redefine board_array to only have boards being used

			#rotate boards
			for b in range(1, len(board_array)):
				r = random.randint(0,5)
				board_array[b] = Setup(board_array[b]).rotate(r)

			starting_spaces = Setup(self.board).determine_starting_spaces()
			random.shuffle(starting_spaces) #shuffle the starting spaces, otherwise cut for P1 and P2 will be the same for any rotation
			cut = random.randint(math.floor(len(starting_spaces)/2), math.ceil(len(starting_spaces)/2)) #cut assumes players play well
			self.P1 = starting_spaces[:cut].copy()
			self.P2 = starting_spaces[cut:].copy()

			#add pieces in P1 and P2 to the board
			for space in self.P1:
				self.board[int(space[1])][int(space[2])]["has_piece"] = "P1" #x=space[1], y=space[2]
			for space in self.P2:
				self.board[int(space[1])][int(space[2])]["has_piece"] = "P2" #x=space[1], y=space[2]

			Setup(self.board).add_sub_dots(board_array)

		self.players = [self.P2, self.P1] #redefine with updated self.P1 and self.P2
		board_array[0] = self.board #redefine top board in board_array


		continue_game = True
		while continue_game:
			print("\n\n\nMOVE NUMBER {}".format(self.turn))
			print(Display(self.board))

			#redefine self.P1 and self.P2 such that neither array includes pieces already in holes
			flat_board = [item for sublist in self.board for item in sublist] #flatten board
			self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1" and not space["is_hole"]] #remove pieces that are already in holes
			self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2" and not space["is_hole"]] #remove pieces that are already in holes
			self.players = [self.P2, self.P1] #redefine with updated self.P1 and self.P2
			self.CP = self.players[self.turn%2] #defines current player based on turn as index of self.players
			CP_name = "P" + str(((self.turn + 1)%2)+1)
			
			#If current player has no legal moves
			if len(self.CP) == 0:
				print("No valid moves for {}".format(CP_name))
				self.turn += 1 #move to next player
				continue; #move to top of loop

			Actions(self.board).take_turn(self.turn, self.CP)

			#check if piece in center, end game if lowest board
			if self.center["has_piece"]:
				if self.board == B1:
					break; #end game
				else:
					print("\n{}'s piece is in the center, they will now move it...\n".format(CP_name))
					print(Display(self.board))
					Actions(self.board).take_turn(self.turn, self.CP)

			if Setup(self.board).check_for_complete_board(): #if all pieces are in holes
				Setup(self.board).imprint_board(board_array[1])

				board_array.pop(0)
				self.board = board_array[0]

				print(len(board_array))

				print("\n\n\nALL SPACES ON BOARD B{} ARE FILLED, MOVING DOWN TO BOARD B{}\n\n\n".format(len(board_array)+1, len(board_array)))

			self.turn += 1

		print("\n\nThere is a winner...\n\n\nTHE WINNER IS: {}".format(self.center["has_piece"]))



def main():
	FullGame(B2).play()

if __name__ == '__main__':
	main()


"""
NEXT STEP:

Debugging

-playing on any one given board is fine, moving down boards causes problems.  

IDEAS:
Create intuitive gameplay for players, GUI?
Create move trees
Create AI to learn game, find optimal strategy
"""



