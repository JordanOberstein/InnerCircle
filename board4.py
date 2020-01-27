#data for board 4
#Copyright Symbol Facing Upwards

B4_Data = {
	"i00": {
		"name": "i00",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i01",
			"br": "i11",
			"bl": "i10",
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i02", "i22", "i33"]
	},
	"i01": {
		"name": "i01",
		"dots": 3,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i02",
			"br": "i12",
			"bl": "i11",
			"l": "i00"
		},
		"sub_dots": False,
		"return_moves": ["i12", "i21", "i40"]
	},
	"i02": {
		"name": "i02",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i03",
			"br": "i13",
			"bl": "i12",
			"l": "i01"
		},
		"sub_dots": False,
		"return_moves": ["i03", "i12", "i22", "i00"]
	},
	"i03": {
		"name": "i03",
		"dots": 1,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": False,
			"br": "i14",
			"bl": "i13",
			"l": "i02"
		},
		"sub_dots": False,
		"return_moves": ["i25", "i33"]
	},
	"i10": {
		"name": "i10",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": "i00",
			"r": "i11",
			"br": "i21",
			"bl": "i20",
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i14", "i20"]
	},
	"i11": {
		"name": "i11",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i00",
			"ur": "i01",
			"r": "i12",
			"br": "i22",
			"bl": "i21",
			"l": "i10"
		},
		"sub_dots": False,
		"return_moves": ["i12", "i13", "i33", "i43"]
	},
	"i12": {
		"name": "i12",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i01",
			"ur": "i02",
			"r": "i13",
			"br": "i23",
			"bl": "i22",
			"l": "i11"
		},
		"sub_dots": False,
		"return_moves": ["i50", "i10"]
	},
	"i13": {
		"name": "i13",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i02",
			"ur": "i03",
			"r": "i14",
			"br": "i24",
			"bl": "i23",
			"l": "i12"
		},
		"sub_dots": False,
		"return_moves": ["i03", "i33", "i12"]
	},
	"i14": {
		"name": "i14",
		"dots": 4,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i03",
			"ur": False,
			"r": False,
			"br": "i25",
			"bl": "i24",
			"l": "i13"
		},
		"sub_dots": False,
		"return_moves": ["i03", "i43"]
	},
	"i20": {
		"name": "i20",
		"dots": 1,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": "i10",
			"r": "i21",
			"br": "i31",
			"bl": "i30",
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i00", "i22", "i30"]
	},
	"i21": {
		"name": "i21",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i10",
			"ur": "i11",
			"r": "i22",
			"br": "i32",
			"bl": "i31",
			"l": "i20"
		},
		"sub_dots": False,
		"return_moves": ["i20"]
	},
	"i22": {
		"name": "i22",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i11",
			"ur": "i12",
			"r": "i23",
			"br": "i33",
			"bl": "i32",
			"l": "i21"
		},
		"sub_dots": False,
		"return_moves": ["i00", "i12", "i02", "i33"]
	},
	"i23": {
		"name": "i23",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i12",
			"ur": "i13",
			"r": "i24",
			"br": "i34",
			"bl": "i33",
			"l": "i22"
		},
		"sub_dots": False,
		"return_moves": ["i12", "i25", "i33", "i21"]
	},
	"i24": {
		"name": "i24",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i13",
			"ur": "i14",
			"r": "i25",
			"br": "i35",
			"bl": "i34",
			"l": "i23"
		},
		"sub_dots": False,
		"return_moves": ["i02", "i45", "i22"]
	},
	"i25": {
		"name": "i25",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i14",
			"ur": False,
			"r": False,
			"br": "i36",
			"bl": "i35",
			"l": "i24"
		},
		"sub_dots": False,
		"return_moves": ["i36"]
	},
	"i30": {
		"name": "i30",
		"dots": 1,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": "i20",
			"r": "i31",
			"br": "i40",
			"bl": False,
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i20", "i10", "i33"]
	},
	"i31": {
		"name": "i31",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i20",
			"ur": "i21",
			"r": "i32",
			"br": "i41",
			"bl": "i40",
			"l": "i30"
		},
		"sub_dots": False,
		"return_moves": ["i20", "i01", "i33", "i41", "i30"]
	},
	"i32": {
		"name": "i32",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i21",
			"ur": "i22",
			"r": "i33",
			"br": "i42",
			"bl": "i41",
			"l": "i31"
		},
		"sub_dots": False,
		"return_moves": ["i10", "i33", "i41"]
	},
	"i33": {
		"name": "i33",
		"dots": "C",
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i22",
			"ur": "i23",
			"r": "i34",
			"br": "i43",
			"bl": "i42",
			"l": "i32"
		},
		"sub_dots": False,
		"return_moves": ["i13", "i63"]
	},
	"i34": {
		"name": "i34",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i23",
			"ur": "i24",
			"r": "i35",
			"br": "i44",
			"bl": "i43",
			"l": "i33"
		},
		"sub_dots": False,
		"return_moves": ["i01", "i44", "i54", "i33"]
	},
	"i35": {
		"name": "i35",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i24",
			"ur": "i25",
			"r": "i36",
			"br": "i45",
			"bl": "i44",
			"l": "i34"
		},
		"sub_dots": False,
		"return_moves": ["i13", "i36", "i44", "i33"]
	},
	"i36": {
		"name": "i36",
		"dots": 1,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i25",
			"ur": False,
			"r": False,
			"br": False,
			"bl": "i45",
			"l": "i35"
		},
		"sub_dots": False,
		"return_moves": ["i54", "i63", "i33"]
	},
	"i40": {
		"name": "i40",
		"dots": 4,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i30",
			"ur": "i31",
			"r": "i41",
			"br": "i50",
			"bl": False,
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i30", "i21", "i41", "i43"]
	},
	"i41": {
		"name": "i41",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i31",
			"ur": "i32",
			"r": "i42",
			"br": "i51",
			"bl": "i50",
			"l": "i40"
		},
		"sub_dots": False,
		"return_moves": ["i22", "i61"]
	},
	"i42": {
		"name": "i42",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i32",
			"ur": "i33",
			"r": "i43",
			"br": "i52",
			"bl": "i51",
			"l": "i41"
		},
		"sub_dots": False,
		"return_moves": ["i21", "i33", "i52", "i62", "i41"]
	},
	"i43": {
		"name": "i43",
		"dots": 3,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i33",
			"ur": "i34",
			"r": "i44",
			"br": "i53",
			"bl": "i52",
			"l": "i42"
		},
		"sub_dots": False,
		"return_moves": ["i33", "i22", "i44", "i45", "i52", "i61"]
	},
	"i44": {
		"name": "i44",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i34",
			"ur": "i35",
			"r": "i45",
			"br": "i54",
			"bl": "i53",
			"l": "i43"
		},
		"sub_dots": False,
		"return_moves": ["i25", "i62", "i40"]
	},
	"i45": {
		"name": "i45",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i35",
			"ur": "i36",
			"r": False,
			"br": False,
			"bl": "i54",
			"l": "i44"
		},
		"sub_dots": False,
		"return_moves": ["i36", "i44"]
	},
	"i50": {
		"name": "i50",
		"dots": 4,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i40",
			"ur": "i41",
			"r": "i51",
			"br": "i60",
			"bl": False,
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i41", "i60"]
	},
	"i51": {
		"name": "i51",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i41",
			"ur": "i42",
			"r": "i52",
			"br": "i61",
			"bl": "i60",
			"l": "i50"
		},
		"sub_dots": False,
		"return_moves": ["i41", "i33", "i52", "i60"]
	},
	"i52": {
		"name": "i52",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i42",
			"ur": "i43",
			"r": "i53",
			"br": "i62",
			"bl": "i61",
			"l": "i51"
		},
		"sub_dots": False,
		"return_moves": ["i14", "i54"]
	},
	"i53": {
		"name": "i53",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i43",
			"ur": "i44",
			"r": "i54",
			"br": "i63",
			"bl": "i62",
			"l": "i52"
		},
		"sub_dots": False,
		"return_moves": ["i33", "i44", "i52"]
	},
	"i54": {
		"name": "i54",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i44",
			"ur": "i45",
			"r": False,
			"br": False,
			"bl": "i63",
			"l": "i53"
		},
		"sub_dots": False,
		"return_moves": ["i44", "i50"]
	},
	"i60": {
		"name": "i60",
		"dots": 1,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i50",
			"ur": "i51",
			"r": "i61",
			"br": False,
			"bl": False,
			"l": False
		},
		"sub_dots": False,
		"return_moves": ["i33", "i62", "i63"]
	},
	"i61": {
		"name": "i61",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i51",
			"ur": "i52",
			"r": "i62",
			"br": False,
			"bl": False,
			"l": "i60"
		},
		"sub_dots": False,
		"return_moves": ["i52", "i60"]
	},
	"i62": {
		"name": "i62",
		"dots": 2,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i52",
			"ur": "i53",
			"r": "i63",
			"br": False,
			"bl": False,
			"l": "i61"
		},
		"sub_dots": False,
		"return_moves": ["i52"]
	},
	"i63": {
		"name": "i63",
		"dots": 3,
		"starting_space": True,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i53",
			"ur": "i54",
			"r": False,
			"br": False,
			"bl": False,
			"l": "i62"
		},
		"sub_dots": False,
		"return_moves": ["i33", "i45", "i61"]
	}
}

B4 = [
	[B4_Data["i00"], B4_Data["i01"], B4_Data["i02"], B4_Data["i03"]], \
	[B4_Data["i10"], B4_Data["i11"], B4_Data["i12"], B4_Data["i13"], B4_Data["i14"]], \
	[B4_Data["i20"], B4_Data["i21"], B4_Data["i22"], B4_Data["i23"], B4_Data["i24"], B4_Data["i25"]], \
	[B4_Data["i30"], B4_Data["i31"], B4_Data["i32"], B4_Data["i33"], B4_Data["i34"], B4_Data["i35"], B4_Data["i36"]], \
	[B4_Data["i40"], B4_Data["i41"], B4_Data["i42"], B4_Data["i43"], B4_Data["i44"], B4_Data["i45"]], \
	[B4_Data["i50"], B4_Data["i51"], B4_Data["i52"], B4_Data["i53"], B4_Data["i54"]], \
	[B4_Data["i60"], B4_Data["i61"], B4_Data["i62"], B4_Data["i63"]]
]
