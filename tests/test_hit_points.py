from dnd_character import Character


def test_level_one_max_hp():
    t = Character(constitution=10)
    assert t.max_hp == 8
    t.hp -= 1
    assert t.hp == t.max_hp - 1


def test_level_ten_max_hp():
    t = Character(level=11, constitution=10)
    assert t.max_hp == 58
