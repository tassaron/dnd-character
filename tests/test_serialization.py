from dnd_character import Character

def test_save_and_load_lvl1_player():
    player = Character()
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)

def test_save_and_load_lvl3_player():
    player = Character(level=3)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)
