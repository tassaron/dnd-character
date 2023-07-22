from dnd_character.classes import (
    CLASSES,
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
    assert barbarian.classs == CLASSES["barbarian"]
    bard = Bard()
    assert bard.classs == CLASSES["bard"]
    cleric = Cleric()
    assert cleric.classs == CLASSES["cleric"]
    druid = Druid()
    assert druid.classs == CLASSES["druid"]
    fighter = Fighter()
    assert fighter.classs == CLASSES["fighter"]
    monk = Monk()
    assert monk.classs == CLASSES["monk"]
    paladin = Paladin()
    assert paladin.classs == CLASSES["paladin"]
    ranger = Ranger()
    assert ranger.classs == CLASSES["ranger"]
    rogue = Rogue()
    assert rogue.classs == CLASSES["rogue"]
    sorcerer = Sorcerer()
    assert sorcerer.classs == CLASSES["sorcerer"]
    warlock = Warlock()
    assert warlock.classs == CLASSES["warlock"]
    wizard = Wizard()
    assert wizard.classs == CLASSES["wizard"]
