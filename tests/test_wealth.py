from dnd_character import Character


def test_character_init_wealth():
    c = Character(wealth=100)
    assert c.wealth == 100


def test_character_increase_wealth():
    c = Character()
    c.giveWealth(100)
    assert c.wealth == 100


def test_character_decrease_wealth_success():
    c = Character(wealth=100)
    assert c.removeWealth(100) == True
    assert c.wealth == 0


def test_character_decrease_wealth_failure():
    c = Character(wealth=100)
    assert c.removeWealth(101) == False
    assert c.wealth == 100
