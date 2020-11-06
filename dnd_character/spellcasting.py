from dnd_character.SRD import SRD, SRD_endpoints


SRD_spells = {
    spell["index"]: SRD(spell["url"])
    for spell in SRD(SRD_endpoints["spells"])["results"]
}

SRD_spells_by_level = {
    i: [key for key, val in SRD_spells.items() if val["level"] == i] for i in range(10)
}
