#move tree for each board

from board1 import B1, B1_Data
from colored import fg, bg, attr
from itertools import permutations
from itertools import product

from paths import create_tree


pathways = {}
spaces = set()
paths = create_tree(B1, B1_Data, spaces)
all_lengths = [(item, pathways[item]["length"]) for item in pathways.keys()]



print("\n\n\n\n\n\n")


#players assigned to each space
players = (sorted(set(permutations(['P1', 'P1', 'P2','P2'], 3))))
# [('P1', 'P1', 'P2'), ('P1', 'P2', 'P1'), ('P1', 'P2', 'P2'), ('P2', 'P1', 'P1'), ('P2', 'P1', 'P2'), ('P2', 'P2', 'P1')]


starting_spaces = ['i21', 'i12', 'i24', 'i44', 'i52', 'i41']
#lengths = [item for item in all_lengths if item[0] in starting_spaces]
lengths = [5, 4, 5, 3, 4, 5]
dots = [2, 4, 2, 4, 2, 4]

#permutations of starting pieces
starting_permutations = [(starting_spaces[(0+r)%6], starting_spaces[(2+r)%6], starting_spaces[(3+r)%6]) for r in range(6)]
#[('i21', 'i24', 'i44'), ('i12', 'i44', 'i52'), ('i24', 'i52', 'i41'), ('i44', 'i41', 'i21'), ('i52', 'i21', 'i12'), ('i41', 'i12', 'i24')]



#create list of tuples
zipped = list(zip(starting_spaces, lengths, dots))

spaces = starting_permutations.copy()

for x in range(6):
	i = []
	for t in range(3):
		for y in range(6):
			if spaces[x][t] == zipped[y][0]:
				i.append(y)
	spaces[x] = [zipped[i[0]], zipped[i[1]], zipped[i[2]]]

#spaces: [[('i21', 5, 2), ('i24', 5, 2), ('i44', 3, 4)], [('i12', 4, 4), ('i44', 3, 4), ('i52', 4, 2)], [('i24', 5, 2), ('i52', 4, 2), ('i41', 5, 4)], [('i44', 3, 4), ('i41', 5, 4), ('i21', 5, 2)], [('i52', 4, 2), ('i21', 5, 2), ('i12', 4, 4)], [('i41', 5, 4), ('i12', 4, 4), ('i24', 5, 2)]]


#36 combinations
combinations = list(product(players, spaces))

#create list of gameplay scenarios
assignments = [list(zip(item[0], item[1])) for item in combinations]


#sort by winning piece
sorted_assignments = assignments.copy()
for i in range(36):
	sorted_assignments[i] = sorted(sorted_assignments[i], key = lambda x: x[0]) #sort by player so P1 breaks ties
	sorted_assignments[i] = sorted(sorted_assignments[i], key = lambda x: x[1][1]) #sort by lowest dot



win_data = {}

for i in range(36):
	raw = assignments[i]
	
	winner = sorted_assignments[i][0][0]
	
	more_pieces = max(set([assignments[i][0][0], assignments[i][1][0], assignments[i][2][0]]), key = [assignments[i][0][0], assignments[i][1][0], assignments[i][2][0]].count) 
	
	more_showing_dots = max(set([assignments[i][0][1][2], assignments[i][1][1][2], assignments[i][2][1][2]]), key = [assignments[i][0][1][2], assignments[i][1][1][2], assignments[i][2][1][2]].count) 
	
	winning_piece = sorted_assignments[i][0][1][0]
	
	winning_dots = sorted_assignments[i][0][1][2]
	
	name = "p{}{}".format(i//6, i%6) #arbitrarily named currently

	pieces = (assignments[i][0][1][0], assignments[i][1][1][0], assignments[i][2][1][0])

	winning_piece_index = pieces.index(winning_piece)


	win_data[name] = {
		"raw": raw,
		"winner": winner,
		"more_pieces": more_pieces,
		"more_showing_dots": more_showing_dots,
		"winning_piece": winning_piece,
		"winning_dots": winning_dots,
		"pieces": pieces,
		"winning_piece_index": winning_piece_index
	}


#create zipped list
winning_spaces = [win_data[item]["winning_piece"] for item in win_data]
winning_permutations = [win_data[item]["pieces"] for item in win_data]
winner = [win_data[item]["winner"] for item in win_data]
winning_dots = [win_data[item]["winning_dots"] for item in win_data]
setup_data = list(zip(winning_spaces, winning_permutations, winner, winning_dots))


for game in win_data:
	DATA = "{}...    ".format(game)
	for item in win_data[game]:
		DATA += ("{}: {}    ".format(item, win_data[game][item]))
	print(DATA)































"""
TO DO LIST:

FIX INTERACTIONS WITH CENTER OF BOARD

ONCE FIXED, ADD PATHWAYS TO BOARD FILES

#this is technically correct for board 1 as no path crosses the center, only ends on the center






def print_tree():
	starting_spaces = ['i21', 'i12', 'i24', 'i44', 'i52', 'i41']
	DATA = ""
	for item0 in tree.keys():
		nest = 0
		tabs = nest * "\t"
		DATA += "{}{}: {{\n".format(tabs, item0)
		for item1 in tree[item0]:
			nest = 1
			tabs = nest * "\t"
			DATA += "{}{}: {{\n".format(tabs, item1)
			for item2 in tree[item0][item1]:
				nest = 2
				tabs = nest * "\t"
				DATA += "{}{}: {{\n".format(tabs, item2)
				for item3 in tree[item0][item1][item2]:
					nest = 3
					tabs = nest * "\t"
					DATA += "{}{}: {{\n".format(tabs, item3)
					for item4 in tree[item0][item1][item2][item3]:
						nest = 4
						tabs = nest * "\t"
						DATA += "{}{}: {{\n".format(tabs, item4)
						for item5 in tree[item0][item1][item2][item3][item4]:
							nest = 5
							tabs = nest * "\t"
							DATA += "{}{}: {{\n".format(tabs, item5)
							for item6 in tree[item0][item1][item2][item3][item4][item5]:
								nest = 6
								tabs = nest * "\t"
								DATA += "{}{}: {{\n".format(tabs, item6)
								DATA += "{}}}\n".format(tabs)
							nest = 5
							tabs = nest * "\t"
							DATA += "{}}}\n".format(tabs)
						nest = 4
						tabs = nest * "\t"
						DATA += "{}}}\n".format(tabs)
					nest = 3
					tabs = nest * "\t"
					DATA += "{}}}\n".format(tabs)
				nest = 2
				tabs = nest * "\t"
				DATA += "{}}}\n".format(tabs)
			nest = 1
			tabs = nest * "\t"
			DATA += "{}}}\n".format(tabs)
		nest = 0
		tabs = nest * "\t"
		DATA += "{}}}\n".format(tabs)

	for space in starting_spaces:
		DATA = DATA.replace(space, colorize(space, 2, 0, 1)) #yellow
	print(DATA)





	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				for item3 in tree[item0][item1][item2]:
					for item4 in tree[item0][item1][item2][item3]:
						for item5 in tree[item0][item1][item2][item3][item4]:
							if item5 in starting_spaces: 
								del tree_copy[item0][item1][item2][item3][item4][item5]
						if item4 in starting_spaces:
							del tree_copy[item0][item1][item2][item3][item4]
					if item3 in starting_spaces:
						del tree_copy[item0][item1][item2][item3]
				if item2 in starting_spaces:
					del tree_copy[item0][item1][item2]
			if item1 in starting_spaces:
				del tree_copy[item0][item1]
		if item0 in starting_spaces:
			del tree_copy[item0][item1][item2][item3][item4][item5]


	for item0 in tree.keys():
		for item1 in tree[item0]:
			for item2 in tree[item0][item1]:
				for item3 in tree[item0][item1][item2]:
					for item4 in tree[item0][item1][item2][item3]:
						for item5 in tree[item0][item1][item2][item3][item4]:
							print(5, item5, item5 not in starting_spaces, len(tree[item0][item1][item2][item3][item4][item5].keys()))
							if item5 not in starting_spaces and len(tree[item0][item1][item2][item3][item4][item5].keys()) == 0:
								del tree[item0][item1][item2][item3][item4][item5]
						print(4, item4, item4 not in starting_spaces, len(tree[item0][item1][item2][item3][item4].keys()))
						if item4 not in starting_spaces and len(tree[item0][item1][item2][item3][item4].keys()) == 0:
							del tree[item0][item1][item2][item3][item4]
					print(3, item3, item3 not in starting_spaces, len(tree[item0][item1][item2][item3].keys()))
					if item3 not in starting_spaces and len(tree[item0][item1][item2][item3].keys()) == 0:
						del tree[item0][item1][item2][item3]
				print(2, item2, item2 not in starting_spaces, len(tree[item0][item1][item2].keys()))
				if item2 not in starting_spaces and len(tree[item0][item1][item2].keys()) == 0:
					del tree[item0][item1][item2]
			print(1, item1, item1 not in starting_spaces, len(tree[item0][item1].keys()))
			if item1 not in starting_spaces and len(tree[item0][item1].keys()) == 0:
				del tree[item0][item1]
		print(0, item0, item0 not in starting_spaces, len(tree[item0].keys()))
		if item0 not in starting_spaces and len(tree[item0].keys()) == 0:
			del tree[item0][item1][item2][item3][item4][item5]


							for item6 in tree[item0][item1][item2][item3][item4][item5]:
								print(5, item5)
								if item6 not in starting_spaces and len(tree[item0][item1][item2][item3][item4][item5][item6].keys()) == 0:
									del tree[item0][item1][item2][item3][item4][item5][item6]


"""
