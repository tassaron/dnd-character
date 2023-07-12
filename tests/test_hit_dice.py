from dnd_character.classes import Barbarian, Rogue, Sorcerer


def test_hd_for_barb_rogue_sorc():
    barb = Barbarian()
    rogue = Rogue()
    sorc = Sorcerer()
    assert barb.hd == 12
    assert rogue.hd == 8
    assert sorc.hd == 6


def test_max_hd_at_level_1():
    barb = Barbarian(level=1)
    assert barb.max_hd == 1


def test_max_hd_at_level_10():
    barb = Barbarian(level=10)
    assert barb.max_hd == 10


def test_current_hd_increases_at_level_up():
    barb = Barbarian(level=1)
    assert barb.current_hd == 1
    barb.level = 2
    assert barb.current_hd == 2
