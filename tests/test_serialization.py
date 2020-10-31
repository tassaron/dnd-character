from dnd_character import Character
from dnd_character.SRD import SRD_classes


def test_save_and_load_lvl1_character():
    player = Character()
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_character():
    player = Character(level=3)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl1_bard():
    player = Character(classs=SRD_classes["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_bard():
    player = Character(level=3, classs=SRD_classes["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)
