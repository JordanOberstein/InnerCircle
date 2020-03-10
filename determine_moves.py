#A script that determines what spaces move to which space, and what spaces receive pieces from each space
#This is found using the adjacent spaces and a recursive function

from board1 import B1, B1_Data
from board2 import B2, B2_Data
from board3 import B3, B3_Data
from board4 import B4, B4_Data


directions = ["ul", "ur", "r", "br", "bl", "l"]
return_moves_data = [{}, {}, {}, {}]
moves_to_data = [{}, {}, {}, {}]
board_array = [B1, B2, B3, B4]
data_array = [B1_Data, B2_Data, B3_Data, B4_Data]


#slightly modified find_move function
def find_move(piece=False, direction=False, moves_remaining=False, board=B1):
    if piece is False:
        return False #not a legal move
    x = int(piece[1]) #row
    y = int(piece[2]) #collumn
    if moves_remaining != 0: #any move that is NOT the final move
        return find_move(board[x][y]["adj"][direction], direction, moves_remaining - 1)
    else:
        return piece


def is_compatible_from(space, new_space, d0, board):
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
        return space == find_move(new_space, d1, dots1, board)


for n in range(4):
    board = board_array[n]

    #add return moves
    for x in range(len(board)):
        for y in range(len(board[x])):
            space = "i{}{}".format(x, y)
            legal_moves = [(find_move(space, d0, dots), d0) for d0 in directions for dots in range(1, 5) if find_move(space, d0, dots)]
            #print("l", legal_moves)
            return_moves = [item[0] for item in legal_moves if is_compatible_from(space, item[0], item[1], board)]
            #print("r", return_moves)
            return_moves_data[n][space] = return_moves
    for item in return_moves_data[n]:
        data_array[n][item]["return_moves"] = return_moves_data[n][item]
        #print(""{}": {}".format(item, return_moves_data[n][item]))
    #print("\n\n")


for n in range(4):
    board = board_array[n]

    #add moves to
    for x in range(len(board)):
        for y in range(len(board[x])):
            piece = "i{}{}".format(x, y)
            dots = board[x][y]["dots"] #number of dots
            if dots == "C": #piece is in center
                dots = [1, 2, 3]
                legal_spaces = [find_move(piece, direction, d, board) for direction in directions for d in dots if find_move(piece, direction, d, board)]
            elif dots == "H":
                legal_spaces = []
            else: #any other space
                legal_spaces = [find_move(piece, direction, dots, board) for direction in directions if find_move(piece, direction, dots, board)]
            moves_to_data[n][piece] = legal_spaces
            #print(legal_spaces)
    #print("\n\n")


for n in range(4):
    for item in return_moves_data[n]:
        print("{} \"return_moves\": {}".format(item, return_moves_data[n][item]))
    print("\n\n")
for n in range(4):
    for item in moves_to_data[n]:
        print("{} \"moves_to\": {}".format(item, moves_to_data[n][item]))
    print("\n\n")


with open("moves.txt", "w") as outfile:
    for n in range(4):
        for item in return_moves_data[n]:
            #outfile.write("{} \"return_moves\": {}\n".format(item, return_moves_data[n][item]))
            outfile.write("\"return_moves\": {}\n".format(return_moves_data[n][item]))
        outfile.write("\n\n")
    for n in range(4):
        for item in moves_to_data[n]:
            #outfile.write("{} \"moves_to\": {}\n".format(item, moves_to_data[n][item]))
            outfile.write("\"moves_to\": {}\n".format(moves_to_data[n][item]))
        outfile.write("\n\n")
