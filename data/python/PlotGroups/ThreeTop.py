# -*- coding: utf-8 -*-
info ={
    "xg": {
        "Name": "X+\gamma", 
        "Members": [
            "wzg",
	        "wwg",
            "ttg_hadronic",
	        "ttg_singleLept",
	        "ttg_dilep",
	        "zg",
            # "wg",
            "tg"
        ]
    },

    "tttt": {
        "Name": r"t\bar{t}t\bar{t}",
        "Members": ["tttt",]
    },

    "ttw": {
        "Name": r"t\bar{t}W", 
        "Members": ["ttw"]
    },
    "ttz": {
        "Name": r"t\bar{t}Z/\gamma*", 
        "Members": ["ttz", "ttz_m1-10"]
    },
    "tth": {
        "Name": r"t\bar{t}H", 
        "Members": ["tth"]
    },

    "ttXY": {
        "Name": r"t\bar{t}VV",
        "Members": [
            "ttww",
	        "ttwz",
	        "ttzz",
	        "tthh",
            "ttzh",
	        "ttwh"
        ]
    },

    "vv": {
        "Name": "vv",
        "Members": [
            "vh2nonbb",
            "zz4l",
            "wpwpjj_ewk",
            "ww_doubleScatter",
            "wzTo3lnu",
        ],
    },
    "vvv": {
        "Name": "vv",
        "Members": [
            "wwz",
            "wzz",
	        "www",
            "zzz",
        ],
    },

    "ttt": {
        "Name": "ttt",
        "Members": ["tttj", "tttw"]
    },

    "other": {
        "Style": "fill-hotpink",
        "Name": "Nonprompt",
        "Members": [
            'ttbar',
            "DYm50",
            "DYm10-50",
            "wjets",
            "tzq",
            # "ttjet"
        ]
    },

    "ttX": {
        "Composite": True,
        "Name": r"t\bar{t}H",
        "Members": [
            "ttw",
            "ttz",
            "tth"
        ]
    },
    "rare": {
        "Composite": True,
        "Name": r"Rare",
        "Members": [
            "vvv",
            "vv",
            "st_twll",
	        "ggh2zz",
        ]
    }

}
