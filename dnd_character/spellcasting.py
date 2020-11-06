from dnd_character.SRD import SRD, SRD_endpoints, SRD_classes


SRD_spells = {
    spell["index"]: SRD(spell["url"])
    for spell in SRD(SRD_endpoints["spells"])["results"]
}

SRD_spells_by_level = {
    i: [key for key, val in SRD_spells.items() if val["level"] == i] for i in range(10)
}

SRD_spells_by_class = {
    i: [
        key
        for key, val in SRD_spells.items()
        if i in (cindex["index"] for cindex in val["classes"])
    ]
    for i in SRD_classes.keys()
}


def spells_for_class_level(classs, level):
    if level > 9 or level < 0:
        raise ValueError("Spell levels only go from 0-9")
    return set(SRD_spells_by_class[classs]).intersection(
        set(SRD_spells_by_level[level])
    )
