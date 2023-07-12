from dnd_character import Character
import pytest


def test_death_dying():
    # dying happens when fails exceed saves
    c = Character()
    c.death_saves = 2
    c.death_fails = 3
    assert c.dead == True and c.death_fails == 0


def test_death_stabilizing():
    # stabilizing (recovering from near-death) happens when saves exceed fails
    c = Character()
    c.death_fails = 2
    c.death_saves = 3
    assert c.dead == False and c.death_fails == 0


def test_death_resets_death_fails():
    c = Character()
    c.death_fails = 2
    c.dead = True
    assert c.death_fails == 0


def test_death_resets_death_saves():
    c = Character()
    c.death_saves = 2
    c.dead = True
    assert c.death_saves == 0


def test_death_saves_upper_range():
    c = Character()
    with pytest.raises(ValueError):
        c.death_saves = 4


def test_death_saves_lower_range():
    c = Character()
    with pytest.raises(ValueError):
        c.death_saves = -1


def test_death_fails_upper_range():
    c = Character()
    with pytest.raises(ValueError):
        c.death_fails = 4


def test_death_fails_lower_range():
    c = Character()
    with pytest.raises(ValueError):
        c.death_fails = -1
