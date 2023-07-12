from dnd_character.character import Character


def test_modifier_zero():
    assert Character.getModifier(10) == 0


def test_modifier_positive():
    assert Character.getModifier(14) == 2


def test_modifier_negative():
    assert Character.getModifier(6) == -2


def test_dexterity_setter_affects_armor_class():
    t = Character(dexterity=10)
    t.dexterity = 12
    assert t.armor_class == 11
