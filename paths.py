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


def colorize(text, atr1, atr2, atr3):
	return '%s%s%s{}'.format(text) % (fg(atr1), bg(atr2), attr(atr3)) + '%s%s%s' % (fg(15), bg(0), attr(0))


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

	update(board, spaces, k)
	k += 1


	#move 1
	new_spaces = set()
	for item0 in tree.keys():
		return_moves = board_data[item0]["return_moves"]
		for space in return_moves:
			if space not in spaces:
				tree[item0][space] = {}
			new_spaces.add(space)
			if space in pathways.keys():
				if pathways[space]["length"] == k:
					pathways[space]["paths"].append([space, item0])
				if pathways[space]["length"] == k-1:
					pathways[space]["sub_paths"].append([space, item1, item0])
			else:
				pathways[space] = {
					"length": k,
					"paths": [[space, item0]],
					"sub_paths": []
				}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
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
				if space in pathways.keys():
					if pathways[space]["length"] == k:
						pathways[space]["paths"].append([space, item1, item0])
					if pathways[space]["length"] == k-1:
						pathways[space]["sub_paths"].append([space, item1, item0])
				else:
					pathways[space] = {
						"length": k,
						"paths": [[space, item1, item0]],
						"sub_paths": []
					}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
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
					if space in pathways.keys():
						if pathways[space]["length"] == k:
							pathways[space]["paths"].append([space, item2, item1, item0])
						if pathways[space]["length"] == k-1:
							pathways[space]["sub_paths"].append([space, item2, item1, item0])
					else:
						pathways[space] = {
							"length": k,
							"paths": [[space, item2, item1, item0]],
							"sub_paths": []
						}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
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
						if space in pathways.keys():
							if pathways[space]["length"] == k:
								pathways[space]["paths"].append([space, item3, item2, item1, item0])
							if pathways[space]["length"] == k-1:
								pathways[space]["sub_paths"].append([space, item3, item2, item1, item0])
						else:
							pathways[space] = {
								"length": k,
								"paths": [[space, item3, item2, item1, item0]],
								"sub_paths": []
							}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
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
							if space in pathways.keys():
								if pathways[space]["length"] == k:
									pathways[space]["paths"].append([space, item4, item3, item2, item1, item0])
								if pathways[space]["length"] == k-1:
									pathways[space]["sub_paths"].append([space, item4, item3, item2, item1, item0])
							else:
								pathways[space] = {
									"length": k,
									"paths": [[space, item4, item3, item2, item1, item0]],
									"sub_paths": []
								}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
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
								if space in pathways.keys():
									if pathways[space]["length"] == k:
										pathways[space]["paths"].append([space, item5, item4, item3, item2, item1, item0])
									if pathways[space]["length"] == k-1:
										pathways[space]["sub_paths"].append([space, item5, item4, item3, item2, item1, item0])
								else:
									pathways[space] = {
										"length": k,
										"paths": [[space, item5, item4, item3, item2, item1, item0]],
										"sub_paths": []
									}
	spaces = spaces | new_spaces #union

	update(board, spaces, k)
	k += 1


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
		paths = create_tree(board_array[n], data_array[n])
		outfile.write(str(paths) + "\n")


"""
TO DO LIST:

FIX INTERACTIONS WITH CENTER OF BOARD
"""
