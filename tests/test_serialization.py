from PyDnD import Player

def test_save_and_load_lvl1_player():
    player = Player()
    clone = Player(**dict(player))
    assert dict(player) == dict(clone)

def test_save_and_load_lvl3_player():
    player = Player(level=3)
    clone = Player(**dict(player))
    assert dict(player) == dict(clone)
