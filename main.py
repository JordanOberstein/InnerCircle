#Based on the game Inner Circle
#By Jordan Oberstein

import random
from board1 import B1
from board2 import B2
from board3 import B3
from board4 import B4

#currently uneeded
#from board1 import O1
#from board1 import O2

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

class Helpers(object):
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

#this is a seperate class from gameplay because gameplay must initialize ONLY once, otherwise random choices get reset
class Actions(object):
	def __init__(self, board):
		self.board = board
		self.directions = ["ul", "ur", "r", "br", "bl", "l"]

	def find_move(self, piece=False, direction=False, moves_remaining=False): #recursive function to find move
		if piece == False:
			return False
		if moves_remaining != 0:
			x = int(piece[1]) #row
			y = int(piece[2]) #collumn
			#print("{} -> {}".format(piece, self.board[x][y]["adj"][direction]), end="\t")
			return Actions(self.board).find_move(self.board[x][y]["adj"][direction], direction, moves_remaining - 1)
		else:
			x = int(piece[1]) #row
			y = int(piece[2]) #collumn
			if self.board[x][y]["has_piece"]: #if the space already contains a piece
				return False
			else:
				return piece

	def legal_moves(self, piece=False):
		if not piece:
			return "Broke"
		x = int(piece[1]) #row
		y = int(piece[2]) #collumn
		dots = self.board[x][y]["dots"] #number of dots
		print("Piece {} moves {} spaces".format(piece, dots))
		legal_spaces = []
		for direction in self.directions:
			legal_spaces.append(Actions(self.board).find_move(piece, direction, dots))
		return legal_spaces

	def take_turn(self, turn, CP):
		CP_name = "P" + str(((turn + 1)%2)+1)

		legal_spaces = []
		while len(legal_spaces) == 0: #will not continue unless the chosen piece has legal moves
			piece_index = input("These are the available pieces for {}, choose 1: {}:\n==> ".format(CP_name, CP)) #"P2" if turn % 2 == 0 else "P1"
			piece = CP[int(piece_index)]
			legal_spaces = [space for space in Actions(self.board).legal_moves(piece) if space != False] #determines legal spaces

		move_index = input("These are the available moves for {}, choose 1: {}:\n==> ".format(piece, legal_spaces))
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

	def determine_starting_spaces(self):
		if self.board == B1:
			r = random.randint(0,5)
			rotated_board_B2 = Helpers(B2).rotate(r) #rotated upper board
			flat_rotated_board_B2 = [item for sublist in rotated_board_B2 for item in sublist] #flatten rotated upper board
			flat_board_B1 = [item for sublist in B1 for item in sublist] #flatten lower board
			#list of indexes of spaces in upper board where spaces are holes
			starting_index_list = [flat_rotated_board_B2.index(item) for item in flat_rotated_board_B2 if item["is_hole"]] 
			return [flat_board_B1[n]["name"] for n in starting_index_list] #spaces in lower board that line up with holes in upper board

class Gameplay(object):
	def __init__(self, board):
		#board
		self.board = board.copy() #prevent any wierd things from hapenning

		#assign pieces and their starting spots to each player randomly
		print("initializing")
		starting_spaces = (Actions(self.board).determine_starting_spaces())
		random.shuffle(starting_spaces) #shuffle the starting spaces, otherwise cuts for P1 and P2 will be the same for any rotation
		cut = random.randint(1, 2)
		self.P1 = starting_spaces[:cut].copy()
		self.P2 = starting_spaces[cut:].copy()
		self.players = [self.P2, self.P1] #index 0, 2, 4 is P2, index 1, 3, 5 is P1

		self.turn = 1 #moves in game; move from P1 + move from P2 = 1 turn

		self.directions = ["ul", "ur", "r", "br", "bl", "l"] #legal directions of movement in adj
		self.center = self.board[3][3] #will have to rework once I add board #2 

	def play_game(self):
		#Gameplay(self.board).setup() #setup the game
		for item in self.P1:
			self.board[int(item[1])][int(item[2])]["has_piece"] = "P1"
		for item in self.P2:
			self.board[int(item[1])][int(item[2])]["has_piece"] = "P2"

		continue_game = True
		while continue_game:
			print("\n\n\nMOVE NUMBER {}".format(self.turn))
			print(Helpers(self.board, ["dots", "has_piece"]))
			self.CP = self.players[self.turn%2] #defines current player based on turn as index of self.players
			if self.center["has_piece"]:
				print("There is a piece in the center")
				continue_game = False
				break; #redundant
			#check if any pieces need to be moved
			if len(self.CP) == 0:
				print("no valid moves for CP")
				self.turn += 1 #move to next player
				continue; #move to top of loop
			Actions(self.board).take_turn(self.turn, self.CP)
			self.turn += 1

		#now that all pieces have holes... (must change this for later board additions)
		return "\n\n\nTHE WINNER IS: {}".format(self.center["has_piece"])






def testing():
	print(Helpers(B1, ["name", "dots", "is_hole", "starting_space"]))
	print(Helpers(B2, ["name", "dots", "is_hole", "starting_space"]))
	print(Helpers(B3, ["name", "dots", "is_hole", "starting_space"]))
	print(Helpers(B4, ["name", "dots", "is_hole", "starting_space"]))


def main():
	"""
	GAME_BOARD = B1.copy()
	print(Helpers(GAME_BOARD, ["adj"]))
	print(Gameplay(GAME_BOARD).play_game())
	"""
	#testing()



	#print(Helpers(B1, ["dots", "name"]))
	#Optimizer(B1).tree_maker()
	#print(Actions(B1).determine_starting_spaces())

if __name__ == '__main__':
	main()


"""
NEXT STEP:


Code tree going outward from center

tree_length = 1
find moves for a piece in center for dots = (x=1,2,3,4) 
if a piece can move x dots from the center onto a space with x dots, then that is a successful move
if pathway lacks array of tree_length 1, 

"""




##CURRENTLY DOES NOT WORK
"""
class Optimizer(object):
	def __init__(self, board):
		self.board = board
		self.center = self.board[3][3]
		self.directions = ["ul", "ur", "r", "br", "bl", "l"] #legal directions of movement in adj
	def tree_maker(self):
		A = [["i33"]]
		length = 0
		while length < 2: 
			A.append([])
			for item in A[length]:
				for dots in range(1, 5):
					for direction in self.directions:
						proposed = Actions(self.board).find_move(item, direction, dots)
						print("length {}, item {}, dots {}, direction {}, proposed {}".format(length, item, dots, direction, proposed))
						if proposed is not False:
							x0 = int(proposed[1]) #row
							y0 = int(proposed[2]) #collumn
							if self.board[x0][y0]["dots"] == dots:
								A[length + 1].append(self.board[x0][y0]["name"])
								print(A)
			length += 1
			print("DONE BREAK")
		print(length)

		while length < 2:
			A.append([])
			for item in A[length]:
				for dots in range(1, 5):
					for direction in self.directions:
						proposed = Actions(self.board).find_move(item, direction, dots)
						print("length {}, item {}, dots {}, direction {}, proposed {}".format(length, item, dots, direction, proposed))
						if proposed is not False:
							x0 = int(proposed[1]) #row
							y0 = int(proposed[2]) #collumn
							if self.board[x0][y0]["dots"] == dots:
								A[1].append(self.board[x0][y0]["name"])
								print(A)
		print(A)
"""

