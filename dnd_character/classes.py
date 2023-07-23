from .SRD import SRD_classes as CLASSES
from .character import Character
from typing import Any


def Barbarian(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["barbarian"], **kwargs)


def Bard(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["bard"], **kwargs)


def Cleric(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["cleric"], **kwargs)


def Druid(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["druid"], **kwargs)


def Fighter(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["fighter"], **kwargs)


def Monk(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["monk"], **kwargs)


def Paladin(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["paladin"], **kwargs)


def Ranger(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["ranger"], **kwargs)


def Rogue(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["rogue"], **kwargs)


def Sorcerer(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["sorcerer"], **kwargs)


def Warlock(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["warlock"], **kwargs)


def Wizard(**kwargs: Any) -> Character:
    return Character(classs=CLASSES["wizard"], **kwargs)
