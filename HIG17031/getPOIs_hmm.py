#!/usr/bin/env python
getPOIs = { 
 
    "L1": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,2], "points":30},
            "lambda_Zg": {"range":[0,3], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "UseWsp": "L1"
    },

    "L1_N1": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": +1.0,
            "lambda_tg": +1.0
        },
        "UseWsp": "L1"
    },
    "L1_N2": {
        "POIs": {
            "lambda_WZ": {"range":[-2,0], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": -1.0,
            "lambda_tg": +1.0
        },
        "UseWsp": "L1"
    },
    "L1_N3": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[-2,0], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": +1.0,
            "lambda_tg": -1.0
        },
        "UseWsp": "L1"
    },
    "L1_N4": {
        "POIs": {
            "lambda_WZ": {"range":[-2,0], "points":40},
            "lambda_tg": {"range":[-2,0], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": -1.0,
            "lambda_tg": -1.0
        },
        "UseWsp": "L1"
    },

    "K1": {
        "POIs": {
            "kappa_W": {"range":[0.2,2.0], "points":30},
            "kappa_Z": {"range":[0.5,1.7], "points":30},
            "kappa_tau": {"range":[0.5,1.8], "points":30},
            "kappa_t": {"range":[0.3,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "BRinv": {"range":[0,0.000000], "points":30}
            },
        "POIsFix": {"BRinv","kappa_mu"},
        "SMVals": { "BRinv": 0.0 }
        },

    "K1_mm": {
        "POIs": {
            "kappa_W": {"range":[0.4,1.7], "points":30},
            "kappa_Z": {"range":[0.4,1.7], "points":30},
            "kappa_tau": {"range":[0.3,1.8], "points":30},
            "kappa_t": {"range":[0.3,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,5.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 }
    },
    "K1_mm_35.9": {
        "POIs": {
            "kappa_W": {"range":[0.4,1.7], "points":30},
            "kappa_Z": {"range":[0.4,1.7], "points":30},
            "kappa_tau": {"range":[0.3,1.8], "points":30},
            "kappa_t": {"range":[0.3,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,5.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 }
    },
    "K1_mm_300": {
        "POIs": {
            "kappa_W": {"range":[0.6,1.4], "points":30},
            "kappa_Z": {"range":[0.6,1.4], "points":30},
            "kappa_tau": {"range":[0.4,1.6], "points":30},
            "kappa_t": {"range":[0.6,1.4], "points":30},
            "kappa_b": {"range":[0.4,1.6], "points":30},
            "kappa_mu": {"range":[0.2,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 }
    },
    "K1_mm_3000": {
        "POIs": {
            "kappa_W": {"range":[0.9,1.15], "points":30},
            "kappa_Z": {"range":[0.9,1.15], "points":30},
            "kappa_tau": {"range":[0.8,1.16], "points":30},
            "kappa_t": {"range":[0.8,1.16], "points":30},
            "kappa_b": {"range":[0.8,1.20], "points":30},
            "kappa_mu": {"range":[0.6,1.4], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 }
    },

    "K1_mm_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_b": +1.0
        }
    },
    "K1_mm_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_b": +1.0
        }
    },
    "K1_mm_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_b": +1.0
        }
    },
    "K1_mm_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_b": +1.0
        }
    },
    "K1_mm_N5": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_b": -1.0
        }
    },
    "K1_mm_N6": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_b": -1.0
        }
    },
    "K1_mm_N7": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_b": -1.0
        }
    },
    "K1_mm_N8": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-1.8,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1_mm",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_b": -1.0
        }
    },
    "K2": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },
    "K2_35.9": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },
    "K2_300": {
        "POIs": {
            "kappa_W": {"range":[0.6,1.4], "points":30},
            "kappa_Z": {"range":[0.6,1.4], "points":30},
            "kappa_mu": {"range":[0.2,2.0], "points":30},
            "kappa_tau": {"range":[0.5,1.5], "points":30},
            "kappa_t": {"range":[0.6,1.4], "points":30},
            "kappa_b": {"range":[0.5,1.5], "points":30},
            "kappa_g": {"range":[0.6,1.4], "points":30},
            "kappa_gam": {"range":[0.7,1.3], "points":30},
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },
    "K2_3000": {
        "POIs": {
            "kappa_W": {"range":[0.9,1.1], "points":30},
            "kappa_Z": {"range":[0.9,1.1], "points":30},
            "kappa_mu": {"range":[0.6,2.0], "points":30},
            "kappa_tau": {"range":[0.8,1.2], "points":30},
            "kappa_t": {"range":[0.8,1.2], "points":30},
            "kappa_b": {"range":[0.8,1.2], "points":30},
            "kappa_g": {"range":[0.9,1.2], "points":30},
            "kappa_gam": {"range":[0.9,1.1], "points":30},
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },
    "K2_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Width": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2Width",
        "SMVals": {"BRinv": 0.0},
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },

    "K2_2D": {
        "POIs": {
            "kappa_g": {"range":[0.4,1.7], "points":30},
            "kappa_gam": {"range":[0.4,1.7], "points":30},
            },
        "POIsFix": {"kappa_W", "kappa_Z","kappa_tau","kappa_t","kappa_b","kappa_mu","BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },

    "K2Inv": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2InvWidth": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0,1.8], "points":30},
            "kappa_tau": {"range":[0,1.8], "points":30},
            "kappa_g": {"range":[0,1.8], "points":30},
            "kappa_gam": {"range":[0,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Inv_2D": {
        "POIs": {
            "kappa_g": {"range":[0.5,1.6], "points":30},
            "kappa_gam": {"range":[0.6,1.5], "points":30},
            "BRinv": {"range":[0,0.9], "points":30}
            },
        "POIsFix":{"kappa_W","kappa_Z","kappa_mu","kappa_tau","kappa_t","kappa_b"}
    },
    "K2Undet": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },

    "K2InvP": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },

    "K2UndetWidth": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Undet_2D": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,2.0], "points":30},
            "kappa_tau": {"range":[0.5,1.8], "points":30},
            "kappa_t": {"range":[0,2.0], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_g": {"range":[0.4,1.7], "points":30},
            "kappa_gam": {"range":[0.5,1.7], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
            },
        "POIsFix":{}
        },
    "K2Undet_Width": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[-0.6,0.6], "points":60}
        },
        "POIsFix":{},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },

    "K2Undet_2Dkgkgam": {
        "POIs": {
            "kappa_g": {"range":[0.5,1.6], "points":30},
            "kappa_gam": {"range":[0.6,1.5], "points":30},
            "BRinv": {"range":[0,0.9], "points":30},
            "BRundet": {"range":[0,0.9], "points":30}
            },
        "POIsFix":{"kappa_W","kappa_Z","kappa_tau","kappa_t","kappa_b","kappa_mu"}
        },

    "K3": { 
        "POIs": {
            "kappa_V": {"range":[0,2], "points":30},
            "kappa_F": {"range":[0,2], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "K3"
        },
 
    "K3_2D": { 
        "POIs": {
            "kappa_V": {"range":[0.6,1.4], "points":30},
            "kappa_F": {"range":[0.6,1.4], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "K3"
        },

    "K3_5D": {
        "POIs": {
            "kappa_V_gamgam": {"range":[0.4,2.5], "points":30},
            "kappa_V_WW": {"range":[0.4,1.8], "points":30},
            "kappa_V_ZZ": {"range":[0.4,1.8], "points":30},
            "kappa_V_mumu": {"range":[0.0,5.0], "points":30},
            "kappa_V_tautau": {"range":[0.4,1.8], "points":30},
            "kappa_V_bb": {"range":[0.4,1.8], "points":30},
            "kappa_F_gamgam": {"range":[0,4.0], "points":30},
            "kappa_F_WW": {"range":[0,4.0], "points":30},
            "kappa_F_ZZ": {"range":[0,2.5], "points":30},
            "kappa_F_mumu": {"range":[0.0,5.0], "points":30},
            "kappa_F_tautau": {"range":[0,2.5], "points":30},
            "kappa_F_bb": {"range":[0,2.5], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"},
        "UseWsp": "K3"
        },

    "K3_5D_2D": {
        "POIs": {

            "kappa_V_gamgam": {"range":[0.7,1.8], "points":30},
            "kappa_V_WW": {"range":[0.5,1.5], "points":30},
            "kappa_V_ZZ": {"range":[0.5,1.5], "points":30},
            "kappa_V_mumu": {"range":[0.3,2.3], "points":30},
            "kappa_V_tautau": {"range":[0.3,2.3], "points":30},
            "kappa_V_bb": {"range":[0.3,2.3], "points":30},
            "kappa_F_gamgam": {"range":[0.5,3.0], "points":30},
            "kappa_F_WW": {"range":[0.5,3.0], "points":30},
            "kappa_F_ZZ": {"range":[0.5,3.0], "points":30},
            "kappa_F_mumu": {"range":[0.5,3.0], "points":30},
            "kappa_F_tautau": {"range":[0.5,1.5], "points":30},
            "kappa_F_bb": {"range":[0.5,1.5], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"},
        "UseWsp": "K3"
        },
    
    "K3_5D_2D_N": { 
        "POIs": {
            "kappa_V_gamgam": {"range":[0.4,1.8], "points":30},
            "kappa_V_WW": {"range":[0.4,1.8], "points":30},
            "kappa_V_ZZ": {"range":[0.4,1.8], "points":30},
            "kappa_V_mumu": {"range":[0.3,2.3], "points":30},
            "kappa_V_tautau": {"range":[0.4,1.8], "points":30},
            "kappa_V_bb": {"range":[0.4,1.8], "points":30},
            "kappa_F_gamgam": {"range":[-2.5,0], "points":30},
            "kappa_F_WW": {"range":[-2.5,0], "points":30},
            "kappa_F_ZZ": {"range":[-2.5,0], "points":30},
            "kappa_F_mumu": {"range":[-2.5,0], "points":30},
            "kappa_F_tautau": {"range":[-2.5,0], "points":30},
            "kappa_F_bb": {"range":[0,2.5], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"}
        },

    "L2_ldu": {
        "POIs": {
            "lambda_du": {"range":[-2,2], "points":40},
            "lambda_Vu": {"range":[-2,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2"
    },

    "L2_ldu_N1": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2_ldu_N2": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2_ldu_N3": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": -1.0
        }
    },
    "L2_ldu_N4": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": -1.0
        }
    },

    "L2flipped_ldu": { 
        "POIs": {
            "lambda_du": {"range":[-2,2], "points":40},
            "lambda_Vu": {"range":[-2,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped"
        },
    
    "L2flipped_ldu_N1": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2flipped_ldu_N2": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2flipped_ldu_N3": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": -1.0
        }
    },
    "L2flipped_ldu_N4": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": -1.0
        }
    },


    "L2_llq": {
        "POIs": {
            "lambda_lq": {"range":[-2,2], "points":40},
            "lambda_Vq": {"range":[-2,2], "points":40},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2"
    },
    "L2_llq_N1": {
        "POIs": {
            "lambda_lq": {"range":[0,2], "points":30},
            "lambda_Vq": {"range":[0,2], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": +1.0,
            "lambda_Vq": +1.0
        }
    },
    "L2_llq_N2": {
        "POIs": {
            "lambda_lq": {"range":[-2,0], "points":30},
            "lambda_Vq": {"range":[0,2], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": -1.0,
            "lambda_Vq": +1.0
        }
    },
    "L2_llq_N3": {
        "POIs": {
            "lambda_lq": {"range":[0,2], "points":30},
            "lambda_Vq": {"range":[-2,0], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": +1.0,
            "lambda_Vq": -1.0
        }
    },
    "L2_llq_N4": {
        "POIs": {
            "lambda_lq": {"range":[-2,0], "points":30},
            "lambda_Vq": {"range":[-2,0], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": -1.0,
            "lambda_Vq": -1.0
        }
    },
    "L2_llq_neg": { 
        "POIs": {
            "lambda_lq": {"range":[-1.8,-0.3], "points":30},
            "lambda_Vq": {"range":[0.4,1.8], "points":30},
            "kappa_qq": {"range":[0.4,1.8], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"}
        },
    
    "L2_lfv": { 
        "POIs": {
            "lambda_FV": {"range":[0,3], "points":30},
            "kappa_VV": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_qq","lambda_lq","lambda_Vq"}
        },

    "A1_5D": { 
        "POIs": {
            "mu_BR_WW": {"range":[0,2], "points":30},
            "mu_BR_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_BR_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_BR_mumu": {"range":[-4.0,4.0], "points":30},
            "mu_BR_tautau": {"range":[0,2.5], "points":30},
            "mu_BR_bb": {"range":[0,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_5P": { 
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.5,2.0], "points":40},
            "mu_XS_VBF": {"range":[0,2], "points":40},
            "mu_XS_WH": {"range":[0,5], "points":40},
            "mu_XS_ZH": {"range":[0,3], "points":40},
            "mu_XS_ttHtH": {"range":[0,3], "points":40}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_ttH": {
        "POIs": {
            "mu_XS_ttH": {"range":[0,5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_ttH_5D": {
        "POIs": {
            "mu_XS_ttH_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS_ttH_BR_ZZ": {"range":[0,10], "points":30},
            "mu_XS_ttH_BR_bb": {"range":[-5,5], "points":30},
            "mu_XS_ttH_BR_gamgam": {"range":[-5,5], "points":30},
            "mu_XS_ttH_BR_tautau": {"range":[-5,5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_ttH_E": {
        "POIs": {
            "mu_XS8_ttH": {"range":[0,5], "points":30},
            "mu_XS13_ttH": {"range":[0,5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_4P": { 
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.5,1.9], "points":30},
            "mu_XS_VBF": {"range":[0,3], "points":30},
            "mu_XS_VH": {"range":[0,3], "points":30},
            "mu_XS_ttHtH": {"range":[0,5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },
    
    "A1_muVmuF": { 
        "POIs": {
            "mu_V_ZZ": {"range":[-2,5], "points":30},
            "mu_V_gamgam": {"range":[0,3], "points":30},
            "mu_V_WW": {"range":[0,3], "points":30},
            "mu_V_tautau": {"range":[0,3], "points":30},
            "mu_V_bb": {"range":[0,3], "points":30},
            "mu_F_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_F_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_F_WW": {"range":[0.0,2.0], "points":30},
            "mu_F_tautau": {"range":[0.0,2.5], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_muVmuF_2D": { 
        "POIs": {
            "mu_V_ZZ": {"range":[-2,4], "points":30},
            "mu_V_gamgam": {"range":[0,5], "points":30},
            "mu_V_WW": {"range":[0,5], "points":30},
            "mu_V_tautau": {"range":[0,5], "points":30},
            "mu_V_bb": {"range":[0,5], "points":30},
            "mu_F_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_F_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_F_WW": {"range":[0.0,2.0], "points":30},
            "mu_F_tautau": {"range":[0.0,2.5], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_mu": { 
        "POIs": {
            "mu": {"range":[0.5,1.5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_5PD": { 
        "POIs": {
            "mu_XS_ggFbbH_BR_WW": {"range":[0.5,2.5], "points":30},
            "mu_XS_VBF_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS_WH_BR_WW": {"range":[-3,15], "points":30},
            "mu_XS_ZH_BR_WW": {"range":[-10,10], "points":30},
            "mu_XS_ttHtH_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS_ggFbbH_BR_ZZ": {"range":[0,2], "points":30},
            "mu_XS_VBF_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_XS_WH_BR_ZZ": {"range":[0,15], "points":30},
            "mu_XS_ZH_BR_ZZ": {"range":[0,20], "points":30},
            "mu_XS_ttHtH_BR_ZZ": {"range":[0,10], "points":30},
            "mu_XS_ggFbbH_BR_bb": {"range":[-5,10], "points":30},
            "mu_XS_WH_BR_bb": {"range":[-4,4], "points":30},
            "mu_XS_ZH_BR_bb": {"range":[-3,3], "points":30},
            "mu_XS_ttHtH_BR_bb": {"range":[-1,3], "points":30},
            "mu_XS_ggFbbH_BR_gamgam": {"range":[0,2], "points":30},
            "mu_XS_VBF_BR_gamgam": {"range":[-1,5], "points":30},
            "mu_XS_WH_BR_gamgam": {"range":[-10,10], "points":30},
            "mu_XS_ZH_BR_gamgam": {"range":[0,15], "points":30},
            "mu_XS_ttHtH_BR_gamgam": {"range":[-1,6], "points":30},
            "mu_XS_ggFbbH_BR_tautau": {"range":[0.1,3.5], "points":30},
            "mu_XS_VBF_BR_tautau": {"range":[0,2.5], "points":30},
#            "mu_XS_WH_BR_tautau": {"range":[-30,30], "points":30},
#            "mu_XS_ZH_BR_tautau": {"range":[-30,30], "points":30},
            "mu_XS_ttHtH_BR_tautau": {"range":[-2,5], "points":30},
            "mu_XS_ggFbbH_BR_mumu": {"range":[-10,10], "points":30},
            "mu_XS_VBF_BR_mumu": {"range":[-15,20], "points":30},
            },
        "POIsFix":{"mu_XS_WH_BR_tautau","mu_XS_ZH_BR_tautau","mu_XS_VBF_BR_bb","mu_XS_WH_BR_mumu","mu_XS_ZH_BR_mumu","mu_XS_ttHtH_BR_mumu"},
        "UseWsp": "A1"
        },
    
    "A2": { 
        "POIs": {
            "mu_V_r_F": {"range":[0,3], "points":30},
            "mu_F_gamgam": {"range":[0,3], "points":30},
            "mu_F_ZZ": {"range":[0,3], "points":30},
            "mu_F_WW": {"range":[0,3], "points":30},
            "mu_F_tautau": {"range":[0,3], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix": {"mu_V_r_F_WW","mu_V_r_F_ZZ","mu_V_r_F_gamgam","mu_V_r_F_bb","mu_V_r_F_tautau"},
        "UseWsp": "A2"
        },

    "A2_5D": { 
        "POIs": {
            "mu_F_gamgam": {"range":[0,5], "points":30},
            "mu_F_ZZ": {"range":[0,5], "points":30},
            "mu_F_WW": {"range":[0,5], "points":30},
            "mu_F_tautau": {"range":[0,5], "points":30},
            "mu_F_bb": {"range":[0,5], "points":30},
            "mu_V_r_F_ZZ": {"range":[0,20], "points":30}
            },
        "POIsFix": {"mu_V_r_F"},
        "UseWsp": "A1"
        },
    
    "B1": {         
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[0.0,2.0], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[0.0,5.0], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-1.0,3.0], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0.0,3.0], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_bb_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_mumu_r_BR_WW": {"range":[0.0,5.0], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_XS_ggF_x_BR_WW": {"range":[0.5,2.0], "points":30}
            }, 
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu","mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"},
        "UseWsp": "B1"
        },

    "B1ZZ": { 
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[0.0,2.0], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[0.0,5.0], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-1.0,3.0], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0.0,3.0], "points":30},
            "mu_BR_WW_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_bb_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_mumu_r_BR_ZZ": {"range":[0.0,5.0], "points":30},
            "mu_BR_tautau_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_gamgam_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_XS_ggF_x_BR_ZZ": {"range":[0.5,2.0], "points":30}
            },
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu","mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        "POIsFix": {"mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"},
        "UseWsp": "B1ZZ"
        },
    
    "B1WW_P78": { 
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[-5,5], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-20,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_bb_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS_ggF_x_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_VBF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_WH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ZH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ggF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_ttH": {"range":[-10,10], "points":30}
            },
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        },

    "B1ZZ_P78": { 
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[-5,5], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-20,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_BR_WW_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_bb_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_tautau_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_gamgam_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_XS_ggF_x_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_VBF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_WH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ZH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ggF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_ttH": {"range":[-10,10], "points":30}
            },
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        },
    
    "B2": { 
        "POIs": {
            "mu_XS_ggF_x_BR_WW": {"range":[0,5], "points":30},
            "mu_XS_VBF_x_BR_tautau": {"range":[0,5], "points":30},
            "mu_XS_WH_r_XS_VBF": {"range":[0,30], "points":30},
            "mu_XS_ZH_r_XS_WH": {"range":[0,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0,10], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_bb_r_BR_tautau": {"range":[0,5], "points":30}
            },
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"}
        "POIsFix": {}
        },

    "D1_general": { 
        "POIs": {
            "mu_WW": {"range":[0,5], "points":30},
            "mu_ZZ": {"range":[0,5], "points":30},
            "mu_gamgam": {"range":[0,5], "points":30},
            "mu_tautau": {"range":[0,5], "points":30},
            "l_VBF_gamgam": {"range":[0,5], "points":30},
            "l_VBF_WW": {"range":[0,5], "points":30},
            "l_VBF_ZZ": {"range":[0,10], "points":30},
            "l_VBF_tautau": {"range":[0,5], "points":30},
            "l_WH_gamgam": {"range":[0,30], "points":30},
            "l_WH_WW": {"range":[0,10], "points":30},
            "l_WH_ZZ": {"range":[0,30], "points":30},
            "l_WH_tautau": {"range":[0,10], "points":30},
            "l_WH_bb": {"range":[0,10], "points":30},
            "l_ZH_gamgam": {"range":[0,10], "points":30},
            "l_ZH_WW": {"range":[0,20], "points":30},
            "l_ZH_ZZ": {"range":[0,50], "points":30},
            "l_ZH_tautau": {"range":[0,20], "points":30},
            "l_ZH_bb": {"range":[0,5], "points":30},
            "l_ttH_gamgam": {"range":[0,20], "points":30},
            "l_ttH_WW": {"range":[0,10], "points":30},
            "l_ttH_ZZ": {"range":[0,50], "points":30},
            "l_ttH_tautau": {"range":[0,30], "points":30},
            "l_ttH_bb": {"range":[0,10], "points":30}
            },
        "POIsFix": {"l_VBF","l_WH","l_ZH","l_ttH","mu_bb"}        
        },

    "D1_rank1": { 
        "POIs": {
            "mu_WW": {"range":[0,5], "points":30},
            "mu_ZZ": {"range":[0,5], "points":30},
            "mu_gamgam": {"range":[0,5], "points":30},
            "mu_tautau": {"range":[0,5], "points":30},
            "mu_bb": {"range":[0,5], "points":30},
            "l_VBF": {"range":[0,5], "points":30},
            "l_WH": {"range":[0,10], "points":30},
            "l_ZH": {"range":[0,10], "points":30},
            "l_ttH": {"range":[0,10], "points":30}
            },
        "POIsFix": {"l_VBF_gamgam","l_VBF_WW","l_VBF_ZZ","l_VBF_tautau","l_WH_gamgam","l_WH_WW","l_WH_ZZ","l_WH_tautau","l_WH_bb","l_ZH_gamgam","l_ZH_WW","l_ZH_ZZ","l_ZH_tautau","l_ZH_bb","l_ttH_gamgam","l_ttH_WW","l_ttH_ZZ","l_ttH_tautau","l_ttH_bb"}
        },

    "stage0": { 
        "POIs": {
             "mu_XS_ggH_x_BR_WW": {"range":[0.0,2.5], "points":30},
             "mu_XS_qqH_x_BR_WW": {"range":[0.0,2.5], "points":30},
             "mu_XS_VH2HQQ_x_BR_WW": {"range":[0.0,15.0], "points":30},
             "mu_XS_QQ2HLNU_x_BR_WW": {"range":[0.0,5.0], "points":30},
             "mu_XS_QQ2HLL_x_BR_WW": {"range":[0.0,5.0], "points":30},
             "mu_XS_ttH_x_BR_WW": {"range":[-1.0,3.0], "points":30},
             "mu_BR_bb_r_BR_WW": {"range":[0.0,3.0], "points":30},
             "mu_BR_tautau_r_BR_WW": {"range":[0.0,2.0], "points":30},
             "mu_BR_ZZ_r_BR_WW": {"range":[0.0,1.5], "points":30},
             "mu_BR_gamgam_r_BR_WW": {"range":[0.3,1.8], "points":30},
             "mu_BR_mumu_r_BR_WW": {"range":[0.0,4.0], "points":30},
            },
        "POIsFix": {"mu_BR_gluglu_r_BR_WW","mu_BR_cc_r_BR_WW","THU_ggH_Mu","THU_ggH_Res","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"},
        "UseWsp": "stage0"
        },

    "stage0ZZ": { 
        "POIs": {
             "mu_XS_ggH_x_BR_ZZ": {"range":[0.4,2.0], "points":30},
             "mu_XS_qqH_x_BR_ZZ": {"range":[0.0,2.5], "points":30},
             "mu_XS_VH2HQQ_x_BR_ZZ": {"range":[0.0,15.0], "points":30},
             "mu_XS_QQ2HLNU_x_BR_ZZ": {"range":[0.0,5.0], "points":30},
             "mu_XS_QQ2HLL_x_BR_ZZ": {"range":[0.0,5.0], "points":30},
             "mu_XS_ttH_x_BR_ZZ": {"range":[-1.0,3.0], "points":30},
             "mu_BR_bb_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
             "mu_BR_tautau_r_BR_ZZ": {"range":[0.0,2.0], "points":30},
             "mu_BR_WW_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
             "mu_BR_gamgam_r_BR_ZZ": {"range":[0.3,1.8], "points":30},
             "mu_BR_mumu_r_BR_ZZ": {"range":[0.0,4.0], "points":30},
            },
        "POIsFix": {"mu_BR_gluglu_r_BR_ZZ","mu_BR_cc_r_BR_ZZ","THU_ggH_Mu","THU_ggH_Res","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"}
        },

    "mEpsHiggs": { 
        "POIs": {
             "M": {"range":[200.0,300.0], "points":30},
             "eps": {"range":[-0.15,0.15], "points":30},
            },
        "POIsFix": {},
        "UseWsp": "mEpsHiggs",
        "SMVals": {
          "M": 246.22,
          "eps": 0.0
          }
        },

}

def GetWsp(model):
    if model in getPOIs and 'UseWsp' in getPOIs[model]:
        return getPOIs[model]['UseWsp']
    else:
        return model

def GetPOIsList(model, sep=',', onlyScanPOIs=False):
    POIs = getPOIs[model]["POIs"].keys()
    if onlyScanPOIs and 'ScanPOIs' in getPOIs[model]:
        POIs = getPOIs[model]['ScanPOIs']
    return sep.join(POIs)

def GetPOIRanges(model):
    poiRanges = ':'.join(['%s=%g,%g' % (POI, d["range"][0], d["range"][1]) for POI, d in getPOIs[model]["POIs"].iteritems()])
    return poiRanges + ':qcdeff=0.0001,1.0:r0p1=0.9,1.4:r1p0=0.8,1.3:r1p1=0.4,0.6:r2p0=1.9,2.3:r2p1=-1.0,-0.3'


def SetSMVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if 'SMVals' in getPOIs[model] and POI in getPOIs[model]['SMVals']:
            defVal = getPOIs[model]['SMVals'][POI]
        set_args.append('%s=%g' % (POI, defVal))
    return ','.join(set_args)

def SetNominalVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if 'POIsNominal' in getPOIs[model] and POI in getPOIs[model]['POIsNominal']:
            defVal = getPOIs[model]['POIsNominal'][POI]
            set_args.append('%s=%g' % (POI, defVal))
    return ','.join(set_args)

def GetFreezeList(model):
    return ','.join(list(getPOIs[model]['POIsFix']) + ['zmod_cat6_ord1_b', 'zmod_cat5_ord1_b', 'zmod_cat11_ord1_b', 'zmod_cat13_ord1_b', 'zmod_cat14_ord1_b'])

def GetGeneratePOIs(model):
    doPOIs = getPOIs[model]["POIs"].keys()
    if 'ScanPOIs' in getPOIs[model]:
        doPOIs = getPOIs[model]['ScanPOIs']
    ret = 'P:n::'
    ret += ':'.join(['%s,%s' % (X,X) for X in doPOIs])
    return ret

def GetMinimizerOpts(label='Default'):
  return '--floatOtherPOIs 1 --useAttributes 1 --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --cminFallbackAlgo "Minuit2,migrad,1:0.1" --cminFallbackAlgo "Minuit2,migrad,0:1.0" --cminFallbackAlgo "Minuit2,migrad,1:1.0" --cminFallbackAlgo "Minuit2,migrad,0:5.0" --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH'

if __name__ == "__main__":
    import sys
    model = getPOIs[sys.argv[1]]

    if sys.argv[2] == '-m':
        print GetWsp(sys.argv[1])

    if sys.argv[2] == '-p':
        print GetPOIsList(sys.argv[1])

    if sys.argv[2] == '-P':
        print GetPOIsList(sys.argv[1], sep=' ', onlyScanPOIs=True)

    if sys.argv[2] == '-r':
        print GetPOIRanges(sys.argv[1])

    if sys.argv[2] == '-s':
        print SetSMVals(sys.argv[1])

    if sys.argv[2] == '-n':
        print SetNominalVals(sys.argv[1])

    if sys.argv[2] == '-f':
        print GetFreezeList(sys.argv[1])

    if sys.argv[2] == '-g':
        print GetGeneratePOIs(sys.argv[1])
    
    if sys.argv[2] == '-F':
        flist = GetFreezeList(sys.argv[1])
        if flist == '':
            print ''
        else:
            print ',' + GetFreezeList(sys.argv[1])

    if sys.argv[2] == '-O':
        print GetMinimizerOpts()
