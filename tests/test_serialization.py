from dnd_character import Character
from dnd_character.SRD import SRD_classes


def test_keys_values():
    char = Character(experience=200)
    for key, val in zip(char.keys(), char.values()):
        assert char[key] == val
    assert dict(zip(char.keys(), char.values())) == dict(char)


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


def test_save_and_load_custom_lvl_character():
    player = Character(level=3, experience=100)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_experience():
    player = Character(experience=100)
    clone = Character(**dict(player))
    assert player._experience._experience == clone._experience._experience
    assert player.experience.to_next_level == clone.experience.to_next_level
