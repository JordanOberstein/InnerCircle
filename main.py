#Based on the game Inner Circle
#By Jordan Oberstein

import random
import math

from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4

#currently uneeded
#from board1 import O1
#from board2 import O2
#from board3 import O3
#from board4 import O4


#Empty board for rotation assignments
empty_board = [[(), (), (), ()], \
			[(), (), (), (), ()], \
		  [(), (), (), (), (), ()], \
		[(), (), (), (), (), (), ()], \
		  [(), (), (), (), (), ()], \
			[(), (), (), (), ()], \
			  [(), (), (), ()]]

def create_board(r1, r2, r3, c): #create board using rings
	nb = empty_board.copy()
	nb[2][2], nb[2][3], nb[3][4], nb[4][3], nb[4][2], nb[3][2] = r1[0], r1[1], r1[2], r1[3], r1[4], r1[5]
	nb[1][1], nb[1][2], nb[1][3], nb[2][4], nb[3][5], nb[4][4] = r2[0], r2[1], r2[2], r2[3], r2[4], r2[5]
	nb[5][3], nb[5][2], nb[5][1], nb[4][1], nb[3][1], nb[2][1] = r2[6], r2[7], r2[8], r2[9], r2[10], r2[11]
	nb[0][0], nb[0][1], nb[0][2], nb[0][3], nb[1][4], nb[2][5] = r3[0], r3[1], r3[2], r3[3], r3[4], r3[5]
	nb[3][6], nb[4][5], nb[5][4], nb[6][3], nb[6][2], nb[6][1] = r3[6], r3[7], r3[8], r3[9], r3[10], r3[11]
	nb[6][0], nb[5][0], nb[4][0], nb[3][0], nb[2][0], nb[1][0] = r3[12], r3[13], r3[14], r3[15], r3[16], r3[17]
	nb[3][3] = c
	return nb

class Display(object):
	def __init__(self, board, args=[]):
		self.board = board
		self.args = args

	def __str__(self):
		DATA = ""
		if len(self.args) == 0: #data dump
			for row in self.board:
				DATA += "{:^60}\n".format(str(row))
		elif self.args == ["adj"]: #checking if all directions in adj are correct
			directions = ["ul", "ur", "r", "br", "bl", "l"]
			for d in directions:
				DATA += "{:^60}\n".format(d)
				for i in range(len(self.board)):
					DATA += "{:^60}".format(str([(self.board[i][j]["adj"][d]) for j in range(len(self.board[i]))]))
					DATA += "{:^60}\n".format(str([(self.board[i][j]["name"]) for j in range(len(self.board[i]))]))
		else:
			for arg in self.args: #name of arg
				DATA += "{:^60}".format(arg)
			DATA += "\n"
			for row in self.board: #board rows
				for arg in self.args:
					DATA += "{:^60}".format(str([(row[j][arg]) for j in range(len(row))]))
				DATA += "\n"
		return DATA


class Setup(object):
	def __init__(self, board): #should only be B4
		self.board = board

	def rotate(self, r=1): #default 1 rotation clockwise
		new_board = self.board #prevents glitches where whole board is written over with one sextant
		for k in range(r):
			ring_1 = [new_board[2][2], new_board[2][3], new_board[3][4], new_board[4][3], new_board[4][2], new_board[3][2]]
			nr1 = [ring_1[(n-1)%len(ring_1)] for n in range(len(ring_1))]
			ring_2 = [new_board[1][1], new_board[1][2], new_board[1][3], new_board[2][4], new_board[3][5], new_board[4][4], \
				new_board[5][3], new_board[5][2], new_board[5][1], new_board[4][1], new_board[3][1], new_board[2][1]]
			nr2 = [ring_2[(n-2)%len(ring_2)] for n in range(len(ring_2))]
			ring_3 = [new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3], new_board[1][4], new_board[2][5], \
				new_board[3][6], new_board[4][5], new_board[5][4], new_board[6][3], new_board[6][2], new_board[6][1], \
				new_board[6][0], new_board[5][0], new_board[4][0], new_board[3][0], new_board[2][0], new_board[1][0]]
			nr3 = [ring_3[(n-3)%len(ring_3)] for n in range(len(ring_3))]
			c = new_board[3][3]
			new_board = create_board(nr1, nr2, nr3, c)
		return new_board

	def check_if_complete(self):
		flat_board = [item for sublist in self.board for item in sublist] #flatten rotated upper board
		return (all([space["has_piece"] for space in flat_board if space["starting_space"]])) #if all starting spaces have a piece

	def add_pieces(self):
		players = ["P2", "P1"] #index 0, 2, 4 is P2, index 1, 3, 5 is P1
		turn = 1
		while not Setup(self.board).check_if_complete():
			CP = players[turn%2]
			print(Display(self.board, ["dots", "has_piece"]))
			flat_board = [item for sublist in self.board for item in sublist] #flatten rotated upper board
			remaining_spaces = [space["name"] for space in flat_board if space["starting_space"] and not space["has_piece"]]
			space_index = input("These are the remaining spaces, choose 1: {}\n==>".format(remaining_spaces))
			chosen_space = remaining_spaces[int(space_index)]
			x = int(chosen_space[1]) #row
			y = int(chosen_space[2]) #collumn
			self.board[x][y]["has_piece"] = CP
			turn += 1
		print(Display(self.board, ["dots", "has_piece"]))
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
		elif self.board == B3: #palying with first, second and third board
			r = random.randint(0,5)
			rotated_board_B4 = Setup(B4).rotate(r) #rotated upper board
			flat_rotated_board_B4 = [item for sublist in rotated_board_B4 for item in sublist] #flatten rotated upper board
			flat_board_B3 = [item for sublist in B3 for item in sublist] #flatten lower board
			#list of indexes of spaces in upper board where spaces are holes
			starting_index_list = [flat_rotated_board_B4.index(item) for item in flat_rotated_board_B4 if item["is_hole"]] 
			return [flat_board_B3[n]["name"] for n in starting_index_list] #spaces in lower board that line up with holes in upper board


#this is a seperate class from gameplay because gameplay must initialize ONLY once, otherwise random choices get reset
class Actions(object):
	def __init__(self, board):
		self.board = board

	def find_move(self, piece=False, direction=False, moves_remaining=False): #recursive function to find move
		if piece == False:
			#print()
			return False #not a legal move
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		if moves_remaining != 0: #any move that is NOT the final move
			#print("{} -> {}".format(piece, self.board[x][y]["adj"][direction]), end="\t")
			return Actions(self.board).find_move(self.board[x][y]["adj"][direction], direction, moves_remaining - 1)
		else:
			#print()
			if self.board[x][y]["has_piece"]: #if the final space already contains a piece
				return False
			else:
				return piece

	def legal_moves(self, piece=False):
		if not piece:
			return "no piece, legal_moves is broken"
		
		directions = ["ul", "ur", "r", "br", "bl", "l"]
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		dots = self.board[x][y]["dots"] #number of dots
		if dots == "C": #piece is in center
			dots = [1, 2, 3]
			print("Piece {} moves {} spaces".format(piece, dots))
			legal_spaces = [Actions(self.board).find_move(piece, direction, d) for direction in directions for d in dots]
		else: #any other space
			print("Piece {} moves {} spaces".format(piece, dots))
			legal_spaces = [Actions(self.board).find_move(piece, direction, dots) for direction in directions]
		
		return legal_spaces

	def take_turn(self, turn, CP):
		CP_name = "P" + str(((turn + 1)%2)+1)

		legal_spaces = []
		center = "i33"
		if center in CP:
			piece = center
			legal_spaces = [space for space in Actions(self.board).legal_moves(piece) if space != False]
		else:
			while len(legal_spaces) == 0: #will not continue unless the chosen piece has legal moves
				piece_index = input("These are the available pieces for {}, choose 1: {}:\n==> ".format(CP_name, CP)) #"P2" if turn % 2 == 0 else "P1"
				piece = CP[int(piece_index)]
				legal_spaces = [space for space in Actions(self.board).legal_moves(piece) if space != False] #determines legal spaces

				#safeguard if piece is already in a hole
				if self.board[int(piece[1])][int(piece[2])]["is_hole"]:
					response = input("Piece {} is already in a hole, are you sure you want to move it?\n==>".format(piece))
					if response != "y":
						legal_spaces = []
						continue;

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


class Full_Game(object):
	def __init__(self, board):
		print("initializing")
		self.board = board.copy() #add .copy() ???
		self.P1 = []
		self.P2 = []
		self.players = [self.P1, self.P2] #index 0, 2, 4 is P2, index 1, 3, 5 is P1
		self.turn = 1 #moves in game; move from P1 + move from P2 = 1 turn
		self.center = self.board[3][3]

	def play(self):
		board_array = [B4, B3, B2, B1] #currently unused

		#Add pieces to board at start of game
		if self.board == B4:
			Setup(B4).add_pieces()
			#retrieve P1 and P2
			flat_board = [item for sublist in self.board for item in sublist] #flatten rotated upper board
			self.P1 = [space["name"] for space in flat_board if space["has_piece"] == "P1"]
			self.P2 = [space["name"] for space in flat_board if space["has_piece"] == "P2"]
		
		elif self.board == B1 or self.board == B2 or self.board == B3:
			board_array = board_array[board_array.index(self.board):] #redefine board_array to only have boards being used

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

		self.players = [self.P2, self.P1] #redefine with updated self.P1 and self.P2

		continue_game = True
		while continue_game:
			print("\n\n\nMOVE NUMBER {}".format(self.turn))
			print(Display(self.board, ["name", "dots", "has_piece"]))
			self.CP = self.players[self.turn%2] #defines current player based on turn as index of self.players
			CP_name = "P" + str(((self.turn + 1)%2)+1)
			if len(self.CP) == 0:
				print("no valid moves for CP")
				self.turn += 1 #move to next player
				continue; #move to top of loop

			Actions(self.board).take_turn(self.turn, self.CP)

			#check if piece in center, end game if lowest board
			if self.center["has_piece"]:
				if self.board == B1:
					break; #end game
				else:
					print("\n{}'s piece is in the center, they will now move it...\n".format(CP_name))
					Actions(self.board).take_turn(self.turn, self.CP)
			
			self.turn += 1

		print("\n\nThere is a winner...\n\n\nTHE WINNER IS: {}".format(self.center["has_piece"]))



def main():
	Full_Game(B1).play()

if __name__ == '__main__':
	main()


"""
NEXT STEP:

better formatting, colors to show pieces in holes (GUI?)

set rotations for boards at start of game
	- when taking move on lower board, same input is then translated through r rotations to new board
add attribute for sub layer dots, assign values to attribute at start of game
fix warning for moving piece out of hole using sub layer dots

figure out how to end layer and move to next board
assign starting spaces to lower board based on pieces in holes
	- if P1 or P2 has no pieces then end the game

"""
