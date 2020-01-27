#A script that determines for each space what spaces can move to the given space

from board1 import B1, B1_Data
from board2 import B2, B2_Data
from board3 import B3, B3_Data
from board4 import B4, B4_Data


directions = ["ul", "ur", "r", "br", "bl", "l"]
data = [{}, {}, {}, {}]
board_array = [B1, B2, B3, B4]
data_array = [B1_Data, B2_Data, B3_Data, B4_Data]


#slightly modified find_move function
def find_move(piece=False, direction=False, moves_remaining=False):
	if piece == False:
		return False #not a legal move
	x = int(piece[1]) #row
	y = int(piece[2]) #collumn
	if moves_remaining != 0: #any move that is NOT the final move
		return find_move(B1[x][y]["adj"][direction], direction, moves_remaining - 1)
	else:
		return piece


def is_compatible(space, new_space, d0, board):
	directions = ["ul", "ur", "r", "br", "bl", "l"]
	d_index = directions.index(d0)
	d1 = directions[(d_index + 3) % 6] #opposite direction
	x = int(new_space[1])
	y = int(new_space[2])
	dots1 = board[x][y]["dots"]
	if dots1 == "H":
		return False
	elif dots1 == "C":
		return True
	else:
		return space == find_move(new_space, d1, dots1)


for n in range(4):
	board = board_array[n]
	for x in range(len(board)):
		for y in range(len(board[x])):
			space = "i{}{}".format(x, y)
			legal_moves = [(find_move(space, d0, dots), d0) for d0 in directions for dots in range(1, 5) if find_move(space, d0, dots)]
			return_moves = [item[0] for item in legal_moves if is_compatible(space, item[0], item[1], board)]
			data[n][space] = return_moves
	for item in data[n]:
		data_array[n][item]["return_moves"] = data[n][item]
		#print("'{}': {}".format(item, data[n][item])
	#print("\n\n")


with open('return_moves_dump.txt', 'w') as outfile:
	for n in range(4):
	    outfile.write(str(data_array[n]) + "\n")
