def convert_value(reg_name, value, ct_ratio):

    # VOLTAGE
    if reg_name.startswith("U"):

        final = value * 0.1
        unit = "V"

    # CURRENT
    elif reg_name.startswith("I"):

        final = value * ct_ratio * 0.001
        unit = "A"

    # ACTIVE POWER
    elif reg_name in [
        "Pt",
        "Pa",
        "Pb",
        "Pc",
        "DmPt"
    ]:

        final = value * ct_ratio * 0.1
        unit = "W"

    # REACTIVE POWER
    elif reg_name.startswith("Q"):

        final = value * ct_ratio * 0.1
        unit = "var"

    # POWER FACTOR
    elif reg_name.startswith("PF"):

        final = value * 0.001
        unit = ""

    # FREQUENCY
    elif reg_name == "Freq":

        final = value * 0.01
        unit = "Hz"

    else:

        final = value
        unit = ""

    return round(final, 2), unit