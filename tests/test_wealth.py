from dnd_character import Character


def test_character_init_wealth():
    c = Character(wealth=100)
    assert c.wealth == 100


def test_character_increase_wealth():
    c = Character({"pp": 0, "gp": 1, "ep": 0, "sp": 1, "cp": 1})
    c.change_wealth(sp=10, conversion=True)
    assert c.wealth == 2.11
    assert c.wealth_detailed == {"pp": 0, "gp": 2, "ep": 0, "sp": 1, "cp": 1}


def test_character_decrease_wealth_success():
    c = Character({"pp": 1, "gp": 1, "ep": 1, "sp": 1, "cp": 1})
    c.change_wealth(pp=-1, gp=-1, ep=-1, sp=-1, cp=-1, conversion=False)
    assert c.wealth == 0
    assert c.wealth_detailed == {"pp": 0, "gp": 0, "ep": 0, "sp": 0, "cp": 0}


def test_character_decrease_wealth_failure():
    c = Character(wealth=100)
    assert c.removeWealth(101) is False
    assert c.wealth == 100
