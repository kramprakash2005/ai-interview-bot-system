STAGE_ORDER = [
    "INTRO",
    "JD",
    "PROJECT",
    "INTERNSHIP",
    "BEHAVIORAL"
]


def get_next_stage(stage):
    try:
        i = STAGE_ORDER.index(stage)
        return STAGE_ORDER[i + 1]
    except:
        return None