




def get_familiarity_exploration_score(user_id):
    return


def get_timelessness_newness_score(user_id):
    return


def get_loyalty_variety_score(user_id):
    return


def get_commonality_uniqueness_score(user_id):
    return


def get_personality_traits(user_id):
    traits = ""

    fe_score = get_familiarity_exploration_score(user_id)
    if fe_score > 0.5:
        traits += "F"
    else:
        traits += "E"
    te_score = get_timelessness_newness_score(user_id)
    if te_score >= 1:
        traits += "N"
    else:
        traits += "T"
    lv_score = get_loyalty_variety_score(user_id)
    if lv_score > 0.5:
        traits += "L"
    else:
        traits += "V"
    cu_score = get_commonality_uniqueness_score(user_id)
    if cu_score > 0.5:
        traits += "C"
    else:
        traits += "U"

    return traits

def get_personality_type(user_id):
    personality_map = {
        "ENVC": 'The Early Adopter',
        "ENLU": 'The Nomad',
        "FNVU": 'The Specialist',
        "FNLC": 'The Enthusiast',
        "FTLC": 'The Connoisseur',
        "FTVU": 'The Deep Diver',
        "FNVC": 'The Fanclubber',
        "ETLC": 'The Top Charter',
        "FTLU": 'The Replayer',
        "FTVC": 'The Jukeboxer',
        "ENLC": "The Voyager",
        "FNLU": "The Devotee",
        "ETLU": "The Maverick",
        "ETVU": "The Time Traveler",
        "ETVC": "The Musicologist",
        "ENVU": "The Adventurer"
    }
    traits = get_personality_traits(user_id)

    return personality_map[traits]

def main():
    return



if __name__ == "__main__":
    main()