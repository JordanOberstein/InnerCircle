#data for board 3
#Copyright Symbol Facing Upwards
#Unused Attributes: starting_space

O3 = {
	"i00": {
		"name": "i00",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i01",
			"br": "i11",
			"bl": "i10",
			"l": False
		}
	},
	"i01": {
		"name": "i01",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i02",
			"br": "i12",
			"bl": "i11",
			"l": "i00"
		}
	},
	"i02": {
		"name": "i02",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": False,
			"ur": False,
			"r": "i03",
			"br": "i13",
			"bl": "i12",
			"l": "i01"
		}
	},
	"i03": {
		"name": "i03",
		"dots": 3,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": False,
			"r": False,
			"br": "i14",
			"bl": "i13",
			"l": "i02"
		}
	},
	"i10": {
		"name": "i10",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": False,
			"ur": "i00",
			"r": "i11",
			"br": "i21",
			"bl": "i20",
			"l": False
		}
	},
	"i11": {
		"name": "i11",
		"dots": 2,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i00",
			"ur": "i01",
			"r": "i12",
			"br": "i22",
			"bl": "i21",
			"l": "i10"
		}
	},
	"i12": {
		"name": "i12",
		"dots": 2,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i01",
			"ur": "i02",
			"r": "i13",
			"br": "i23",
			"bl": "i22",
			"l": "i11"
		}
	},
	"i13": {
		"name": "i13",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i02",
			"ur": "i03",
			"r": "i14",
			"br": "i24",
			"bl": "i23",
			"l": "i12"
		}
	},
	"i14": {
		"name": "i14",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i03",
			"ur": False,
			"r": False,
			"br": "i25",
			"bl": "i24",
			"l": "i13"
		}
	},
	"i20": {
		"name": "i20",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": False,
			"ur": "i10",
			"r": "i21",
			"br": "i31",
			"bl": "i30",
			"l": False
		}
	},
	"i21": {
		"name": "i21",
		"dots": 3,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i10",
			"ur": "i11",
			"r": "i22",
			"br": "i32",
			"bl": "i31",
			"l": "i20"
		}
	},
	"i22": {
		"name": "i22",
		"dots": 1,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i11",
			"ur": "i12",
			"r": "i23",
			"br": "i33",
			"bl": "i32",
			"l": "i21"
		}
	},
	"i23": {
		"name": "i23",
		"dots": 2,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i12",
			"ur": "i13",
			"r": "i24",
			"br": "i34",
			"bl": "i33",
			"l": "i22"
		}
	},
	"i24": {
		"name": "i24",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i13",
			"ur": "i14",
			"r": "i25",
			"br": "i35",
			"bl": "i34",
			"l": "i23"
		}
	},
	"i25": {
		"name": "i25",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i14",
			"ur": False,
			"r": False,
			"br": "i36",
			"bl": "i35",
			"l": "i24"
		}
	},
	"i30": {
		"name": "i30",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": False,
			"ur": "i20",
			"r": "i31",
			"br": "i40",
			"bl": False,
			"l": False
		}
	},
	"i31": {
		"name": "i31",
		"dots": 2,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i20",
			"ur": "i21",
			"r": "i32",
			"br": "i41",
			"bl": "i40",
			"l": "i30"
		}
	},
	"i32": {
		"name": "i32",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i21",
			"ur": "i22",
			"r": "i33",
			"br": "i42",
			"bl": "i41",
			"l": "i31"
		}
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
		}
	},
	"i34": {
		"name": "i34",
		"dots": 1,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i23",
			"ur": "i24",
			"r": "i35",
			"br": "i44",
			"bl": "i43",
			"l": "i33"
		}
	},
	"i35": {
		"name": "i35",
		"dots": 2,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i24",
			"ur": "i25",
			"r": "i36",
			"br": "i45",
			"bl": "i44",
			"l": "i34"
		}
	},
	"i36": {
		"name": "i36",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i25",
			"ur": False,
			"r": False,
			"br": False,
			"bl": "i45",
			"l": "i35"
		}
	},
	"i40": {
		"name": "i40",
		"dots": 4,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i30",
			"ur": "i31",
			"r": "i41",
			"br": "i50",
			"bl": False,
			"l": False
		}
	},
	"i41": {
		"name": "i41",
		"dots": 3,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i31",
			"ur": "i32",
			"r": "i42",
			"br": "i51",
			"bl": "i50",
			"l": "i40"
		}
	},
	"i42": {
		"name": "i42",
		"dots": 3,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i32",
			"ur": "i33",
			"r": "i43",
			"br": "i52",
			"bl": "i51",
			"l": "i41"
		}
	},
	"i43": {
		"name": "i43",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i33",
			"ur": "i34",
			"r": "i44",
			"br": "i53",
			"bl": "i52",
			"l": "i42"
		}
	},
	"i44": {
		"name": "i44",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i34",
			"ur": "i35",
			"r": "i45",
			"br": "i54",
			"bl": "i53",
			"l": "i43"
		}
	},
	"i45": {
		"name": "i45",
		"dots": 1,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i35",
			"ur": "i36",
			"r": False,
			"br": False,
			"bl": "i54",
			"l": "i44"
		}
	},
	"i50": {
		"name": "i50",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i40",
			"ur": "i41",
			"r": "i51",
			"br": "i60",
			"bl": False,
			"l": False
		}
	},
	"i51": {
		"name": "i51",
		"dots": 1,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i41",
			"ur": "i42",
			"r": "i52",
			"br": "i61",
			"bl": "i60",
			"l": "i50"
		}
	},
	"i52": {
		"name": "i52",
		"dots": 3,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i42",
			"ur": "i43",
			"r": "i53",
			"br": "i62",
			"bl": "i61",
			"l": "i51"
		}
	},
	"i53": {
		"name": "i53",
		"dots": 4,
		"starting_space": True, #is potential starting space
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i43",
			"ur": "i44",
			"r": "i54",
			"br": "i63",
			"bl": "i62",
			"l": "i52"
		}
	},
	"i54": {
		"name": "i54",
		"dots": 4,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i44",
			"ur": "i45",
			"r": False,
			"br": False,
			"bl": "i63",
			"l": "i53"
		}
	},
	"i60": {
		"name": "i60",
		"dots": 2,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i50",
			"ur": "i51",
			"r": "i61",
			"br": False,
			"bl": False,
			"l": False
		}
	},
	"i61": {
		"name": "i61",
		"dots": 4,
		"starting_space": False,
		"has_piece": False,
		"is_hole": False,
		"adj": {
			"ul": "i51",
			"ur": "i52",
			"r": "i62",
			"br": False,
			"bl": False,
			"l": "i60"
		}
	},
	"i62": {
		"name": "i62",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i52",
			"ur": "i53",
			"r": "i63",
			"br": False,
			"bl": False,
			"l": "i61"
		}
	},
	"i63": {
		"name": "i63",
		"dots": "H",
		"starting_space": False,
		"has_piece": False,
		"is_hole": True,
		"adj": {
			"ul": "i53",
			"ur": "i54",
			"r": False,
			"br": False,
			"bl": False,
			"l": "i62"
		}
	}
}

B3 =	[[O3["i00"], O3["i01"], O3["i02"], O3["i03"]], \
		[O3["i10"], O3["i11"], O3["i12"], O3["i13"], O3["i14"]], \
		[O3["i20"], O3["i21"], O3["i22"], O3["i23"], O3["i24"], O3["i25"]], \
		[O3["i30"], O3["i31"], O3["i32"], O3["i33"], O3["i34"], O3["i35"], O3["i36"]], \
		[O3["i40"], O3["i41"], O3["i42"], O3["i43"], O3["i44"], O3["i45"]], \
		[O3["i50"], O3["i51"], O3["i52"], O3["i53"], O3["i54"]], \
		[O3["i60"], O3["i61"], O3["i62"], O3["i63"]]]

