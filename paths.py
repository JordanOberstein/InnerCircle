#move tree for each board

from board1 import B1, B1_Data
from board2 import B2, B2_Data
from board3 import B3, B3_Data
from board4 import B4, B4_Data

from colored import fg, bg, attr


def print_tree():
	for item0 in tree.keys():
		nest = 0
		tabs = nest * "\t"
		print("{}{}: {{".format(tabs, item0))
		for item1 in tree[item0]:
			nest = 1
			tabs = nest * "\t"
			print("{}{}: {{".format(tabs, item1))
			for item2 in tree[item0][item1]:
				nest = 2
				tabs = nest * "\t"
				print("{}{}: {{".format(tabs, item2))
				for item3 in tree[item0][item1][item2]:
					nest = 3
					tabs = nest * "\t"
					print("{}{}: {{".format(tabs, item3))
					for item4 in tree[item0][item1][item2][item3]:
						nest = 4
						tabs = nest * "\t"
						print("{}{}: {{".format(tabs, item4))
						for item5 in tree[item0][item1][item2][item3][item4]:
							nest = 5
							tabs = nest * "\t"
							print("{}{}: {{".format(tabs, item5))
							for item6 in tree[item0][item1][item2][item3][item4][item5]:
								nest = 6
								tabs = nest * "\t"
								print("{}{}: {{".format(tabs, item6))
								print("{}}}".format(tabs))
							nest = 5
							tabs = nest * "\t"
							print("{}}}".format(tabs))
						nest = 4
						tabs = nest * "\t"
						print("{}}}".format(tabs))
					nest = 3
					tabs = nest * "\t"
					print("{}}}".format(tabs))
				nest = 2
				tabs = nest * "\t"
				print("{}}}".format(tabs))
			nest = 1
			tabs = nest * "\t"
			print("{}}}".format(tabs))
		nest = 0
		tabs = nest * "\t"
		print("{}}}".format(tabs))


def colorize(text, foreground, background, attribute):
	return '{}{}{}{}'.format(fg(foreground), bg(background), attr(attribute), text) + '{}{}{}'.format(fg(15), bg(0), attr(0))


def print_board(board, spaces, dots=False):
	DATA = ""
	for row in board: #board rows
		new_line = str([(space["name"]) for space in row])
		if dots:
			new_line = str([(space["name"], space["dots"]) for space in row])
		new_line = new_line.replace("'", "") #flush formatting
		new_line = new_line.replace("), (", ") (") #flush formatting
		DATA += "{:^80}\n".format(new_line)

	for item in spaces:
		DATA = DATA.replace(item, colorize(item, 2, 0, 4)) #green
	DATA = DATA.replace("C", colorize("C", 3, 0, 1)) #yellow
	DATA = DATA.replace("H", colorize("H", 4, 0, 1)) #blue

	print_data_array.append(DATA)
	print(DATA)


def update(board, spaces, k):
	print("MOVE {}\n".format(k))
	print_tree()
	print_board(board, spaces, True)
	print("\nLength {}: {}\n\n\n".format(len(spaces), spaces))


def create_tree(board, board_data, spaces=set(), k=0):
	center = board[3][3]


	#move 0
	flat_board = [item for sublist in board for item in sublist] #flatten board
	finishing_spaces = [space["name"] for space in flat_board if space["is_hole"]]

	for item in finishing_spaces:
		tree[item] = {}
		spaces.add(item)
		pathways[item] = {
			"length": k,
			"paths": [[item]],
			"sub_paths": []
		}

	#update(board, spaces, k)
	k += 1


	#move 1
	new_spaces = set()
	for item0 in tree.keys():
		return_moves = board_data[item0]["return_moves"]
		for space in return_moves:
			if space not in spaces:
				tree[item0][space] = {}
			new_spaces.add(space)
			path = [space, item0]
			if space in pathways.keys():
				if pathways[space]["length"] == k:
					pathways[space]["paths"].append(path)
				if pathways[space]["length"] == k-1:
					pathways[space]["sub_paths"].append(path)
			else:
				pathways[space] = {
					"length": k,
					"paths": [path],
					"sub_paths": []
				}
	spaces = spaces | new_spaces #union

	#update(board, spaces, k)
	k += 1


	#move 2
	new_spaces = set()
	for item0 in tree.keys():
		for item1 in tree[item0]:
			return_moves = board_data[item1]["return_moves"]
			for space in return_moves:
				if space not in spaces:
					tree[item0][item1][space] = {}
				new_spaces.add(space)
				path = [space, item1, item0]
				if space in pathways.keys():
					if pathways[space]["length"] == k:
						pathways[space]["paths"].append(path)
					if pathways[space]["length"] == k-1:
						pathways[space]["sub_paths"].append(path)
				else:
					pathways[space] = {
						"length": k,
						"paths": [path],
						"sub_paths": []
					}
	spaces = spaces | new_spaces #union

	#update(board, spaces, k)
	k += 1


	#move 3
	new_spaces = set()
	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				return_moves = board_data[item2]["return_moves"]
				for space in return_moves:
					if space not in spaces:
						tree[item0][item1][item2][space] = {}
					new_spaces.add(space)
					path = [space, item2, item1, item0]
					if space in pathways.keys():
						if pathways[space]["length"] == k:
							pathways[space]["paths"].append(path)
						if pathways[space]["length"] == k-1:
							pathways[space]["sub_paths"].append(path)
					else:
						pathways[space] = {
							"length": k,
							"paths": [path],
							"sub_paths": []
						}
	spaces = spaces | new_spaces #union

	#update(board, spaces, k)
	k += 1


	#move 4
	new_spaces = set()
	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				for item3 in tree[item0][item1][item2]:
					return_moves = board_data[item3]["return_moves"]
					for space in return_moves:
						if space not in spaces:
							tree[item0][item1][item2][item3][space] = {}
						new_spaces.add(space)
						path = [space, item3, item2, item1, item0]
						if space in pathways.keys():
							if pathways[space]["length"] == k:
								pathways[space]["paths"].append(path)
							if pathways[space]["length"] == k-1:
								pathways[space]["sub_paths"].append(path)
						else:
							pathways[space] = {
								"length": k,
								"paths": [path],
								"sub_paths": []
							}
	spaces = spaces | new_spaces #union

	#update(board, spaces, k)
	k += 1


	#move 5
	new_spaces = set()
	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				for item3 in tree[item0][item1][item2]:
					for item4 in tree[item0][item1][item2][item3]:
						return_moves = board_data[item4]["return_moves"]
						for space in return_moves:
							if space not in spaces:
								tree[item0][item1][item2][item3][item4][space] = {}
							new_spaces.add(space)
							path = [space, item4, item3, item2, item1, item0]
							if space in pathways.keys():
								if pathways[space]["length"] == k:
									pathways[space]["paths"].append(path)
								if pathways[space]["length"] == k-1:
									pathways[space]["sub_paths"].append(path)
							else:
								pathways[space] = {
									"length": k,
									"paths": [path],
									"sub_paths": []
								}
	spaces = spaces | new_spaces #union

	#update(board, spaces, k)
	k += 1

	#move 6
	new_spaces = set()
	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				for item3 in tree[item0][item1][item2]:
					for item4 in tree[item0][item1][item2][item3]:
						for item5 in tree[item0][item1][item2][item3][item4]:
							return_moves = board_data[item5]["return_moves"]
							for space in return_moves:
								if space not in spaces:
									tree[item0][item1][item2][item3][item4][item5][space] = {}
								new_spaces.add(space)
								path = [space, item5, item4, item3, item2, item1, item0]
								if space in pathways.keys():
									if pathways[space]["length"] == k:
										pathways[space]["paths"].append(path)										
									if pathways[space]["length"] == k-1:
										pathways[space]["sub_paths"].append(path)
								else:
									pathways[space] = {
										"length": k,
										"paths": [path],
										"sub_paths": []
									}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
	k += 1

	if len(print_data_array) > 1:
		print("\n\nFINAL PROGRESSION:\n")
		for i in range(len(print_data_array)):
			print("MOVE {}".format(i))
			print(print_data_array[i])

	for item in pathways:
		print("{}: {}".format(item, pathways[item]))

	return pathways



board_array = [B1, B2, B3, B4]
data_array = [B1_Data, B2_Data, B3_Data, B4_Data]

with open('pathways_dump.txt', 'w') as outfile:
	for n in range(4):
		tree = {}
		pathways = {}
		print_data_array = []
		spaces = set()
		paths = create_tree(board_array[n], data_array[n], spaces)
		outfile.write(str(paths) + "\n")
		outfile.write(str(sorted([(item, pathways[item]["length"]) for item in pathways.keys()])) + "\n")


"""
TO DO LIST:

FIX INTERACTIONS WITH CENTER OF BOARD

ONCE FIXED, ADD PATHWAYS TO BOARD FILES

#this is technically correct for board 1 as no path crosses the center, only ends on the center

"""



print("\n\n\n\n")

l1=[('i00', 1), ('i01', 4), ('i02', 4), ('i03', 3), ('i10', 2), ('i11', 1), ('i12', 4), ('i13', 9), ('i14', 2), ('i20', 3), ('i21', 5), ('i22', 3), ('i23', 4), ('i24', 3), ('i25', 3), ('i30', 3), ('i31', 4), ('i32', 5), ('i33', 0), ('i34', 3), ('i35', 5), ('i36', 3), ('i40', 4), ('i41', 5), ('i42', 5), ('i43', 2), ('i44', 5), ('i45', 4), ('i50', 3), ('i51', 9), ('i52', 4), ('i53', 2), ('i54', 4), ('i60', 4), ('i61', 5), ('i62', 6), ('i63', 1)]
l2=[('i00', 4), ('i01', 3), ('i02', 4), ('i03', 3), ('i10', 4), ('i11', 1), ('i12', 1), ('i13', 1), ('i14', 4), ('i20', 4), ('i21', 0), ('i22', 3), ('i23', 3), ('i24', 0), ('i25', 3), ('i30', 3), ('i31', 2), ('i32', 4), ('i33', 2), ('i34', 2), ('i35', 4), ('i36', 4), ('i40', 3), ('i41', 3), ('i42', 2), ('i43', 5), ('i44', 0), ('i45', 4), ('i50', 4), ('i51', 3), ('i52', 3), ('i53', 2), ('i54', 2), ('i60', 4), ('i61', 4), ('i62', 3), ('i63', 3)]
l3=[('i00', 1), ('i01', 1), ('i02', 0), ('i03', 2), ('i10', 0), ('i11', 2), ('i12', 1), ('i13', 2), ('i14', 1), ('i20', 1), ('i21', 3), ('i22', 2), ('i23', 1), ('i24', 2), ('i25', 0), ('i30', 0), ('i31', 2), ('i32', 3), ('i33', 1), ('i34', 2), ('i35', 2), ('i36', 2), ('i40', 2), ('i41', 2), ('i42', 1), ('i43', 2), ('i44', 2), ('i45', 2), ('i50', 0), ('i51', 1), ('i52', 3), ('i53', 3), ('i54', 1), ('i60', 1), ('i61', 2), ('i62', 0), ('i63', 0)]
l4=[('i00', 2), ('i01', 1), ('i02', 1), ('i03', 2), ('i10', 1), ('i11', 0), ('i12', 1), ('i13', 1), ('i14', 2), ('i20', 1), ('i21', 1), ('i22', 1), ('i23', 0), ('i24', 0), ('i25', 1), ('i30', 1), ('i31', 0), ('i32', 0), ('i33', 1), ('i34', 0), ('i35', 0), ('i36', 1), ('i40', 2), ('i41', 1), ('i42', 0), ('i43', 1), ('i44', 1), ('i45', 1), ('i50', 2), ('i51', 0), ('i52', 1), ('i53', 0), ('i54', 1), ('i60', 1), ('i61', 2), ('i62', 1), ('i63', 2)]

L1 = [l1[:4], l1[4:9], l1[9:15], l1[15:22], l1[22:28], l1[28:33], l1[33:37]]
L2 = [l2[:4], l2[4:9], l2[9:15], l2[15:22], l2[22:28], l2[28:33], l2[33:37]]
L3 = [l3[:4], l3[4:9], l3[9:15], l3[15:22], l3[22:28], l3[28:33], l3[33:37]]
L4 = [l4[:4], l4[4:9], l4[9:15], l4[15:22], l4[22:28], l4[28:33], l4[33:37]]


ls = [L1, L2, L3, L4]

def print_board2(board):
	for x in range(len(board)):
		for y in range(len(board[x])):
			board[x][y] = board[x][y][1]

	DATA = ""
	for row in board:
		newline = str(row)
		newline = newline.replace("'", "").replace("), (", ") (")
		DATA += "{:^80}\n".format(newline)
	print(DATA)

for item in ls:
	print_board2(item)
