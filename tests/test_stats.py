from dnd_character.character import Character

def test_modifier_zero():
    assert Character.getModifier(10) == 0


def test_modifier_positive():
    assert Character.getModifier(14) == 2


def test_modifier_positive():
    assert Character.getModifier(6) == -2
