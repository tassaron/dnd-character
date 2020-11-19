from dnd_character import Character


def test_death_dying():
    c = Character()
    c.death_saves = 2
    c.death_fails = 3
    assert c.dead == True and c.death_fails == 0


def test_death_stabilizing():
    c = Character()
    c.death_fails = 2
    c.death_saves = 3
    assert c.dead == False and c.death_fails == 0
