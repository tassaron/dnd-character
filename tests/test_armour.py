from dnd_character import Character
from dnd_character.classes import Bard, Paladin


def test_armour_class():
    t = Character(dexterity=14)
    assert t.armour_class == 12


def test_light_armour_class():
    t = Bard(dexterity=14)
    assert t.armour_class == 13


def test_heavy_armour_class():
    t = Paladin(dexterity=14)
    assert t.armour_class == 16


def test_heavy_armour_class_ignores_dexterity_change():
    t = Paladin(dexterity=14)
    t.dexterity = 16
    assert t.armour_class == 16


def test_light_armour_still_applies_after_dexterity_change():
    t = Bard(dexterity=14)
    t.dexterity = 16
    assert t.armour_class == 14
