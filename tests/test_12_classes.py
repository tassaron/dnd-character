from dnd_character.classes import (
    Barbarian,
    Bard,
    Cleric,
    Druid,
    Fighter,
    Monk,
    Paladin,
    Ranger,
    Rogue,
    Sorcerer,
    Warlock,
    Wizard,
)


def test_all_12_classes():
    barbarian = Barbarian()
    bard = Bard()
    cleric = Cleric()
    druid = Druid()
    fighter = Fighter()
    monk = Monk()
    paladin = Paladin()
    ranger = Ranger()
    rogue = Rogue()
    sorcerer = Sorcerer()
    warlock = Warlock()
    wizard = Wizard()
    assert wizard.classs
