# =========================
# HOLDING REGISTER
# =========================
holding_registers = {

    "REV": 0x0000,
    "UCode": 0x0001,
    "ClrE": 0x0002,
    "net": 0x0003,

    "RES1": 0x0004,
    "RES2": 0x0005,

    "IrAt": 0x0006,
    "UrAt": 0x0007,

    "MeterType": 0x000B,

    "Protocol": 0x002C,
    "Addr": 0x002D,
    "bAud": 0x002E,

    "Second": 0x002F,
    "Minute": 0x0030,
    "Hour": 0x0031,
    "Day": 0x0032,
    "Month": 0x0033,
    "Year": 0x0034,
}

# =========================
# INPUT REGISTER
# =========================
registers = {

    "Uab": 0x2000,
    "Ubc": 0x2002,
    "Uca": 0x2004,

    "Ua": 0x2006,
    "Ub": 0x2008,
    "Uc": 0x200A,

    "Ia": 0x200C,
    "Ib": 0x200E,
    "Ic": 0x2010,

    "Pt": 0x2012,
    "Pa": 0x2014,
    "Pb": 0x2016,
    "Pc": 0x2018,

    "Qt": 0x201A,
    "Qa": 0x201C,
    "Qb": 0x201E,
    "Qc": 0x2020,

    "PFt": 0x2022,
    "PFa": 0x2024,
    "PFb": 0x2026,
    "PFc": 0x2028,

    "Freq": 0x2044,

    "DmPt": 0x2050,

    # =========================
    # ENERGY
    # =========================
    "ImpEp": 0x401E,
    "ExpEp": 0x4028,

    "Q1Eq": 0x4032,
    "Q2Eq": 0x403C,
    "Q3Eq": 0x4046,
    "Q4Eq": 0x4050,
}