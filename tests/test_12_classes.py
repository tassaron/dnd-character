from dnd_character.character import Character
from dnd_character.classes import (
    SRD_classes,
    CLASSES,
    _CLASS,
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


def test_class_dataclass_dict_interchangeable():
    assert CLASSES["barbarian"] == _CLASS(**SRD_classes["barbarian"])


def test_instantiate_with_dict():
    # ensure that outdated data in dict format gets converted to a dataclass
    cleric = Character(classs=SRD_classes["cleric"])
    assert cleric.classs == CLASSES["cleric"]


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
