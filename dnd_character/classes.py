from .SRD import SRD_classes as CLASSES
from .character import Character


def Barbarian(**kwargs):
    return Character(classs=CLASSES["barbarian"], **kwargs)


def Bard(**kwargs):
    return Character(classs=CLASSES["bard"], **kwargs)


def Cleric(**kwargs):
    return Character(classs=CLASSES["cleric"], **kwargs)


def Druid(**kwargs):
    return Character(classs=CLASSES["druid"], **kwargs)


def Fighter(**kwargs):
    return Character(classs=CLASSES["fighter"], **kwargs)


def Monk(**kwargs):
    return Character(classs=CLASSES["monk"], **kwargs)


def Paladin(**kwargs):
    return Character(classs=CLASSES["paladin"], **kwargs)


def Ranger(**kwargs):
    return Character(classs=CLASSES["ranger"], **kwargs)


def Rogue(**kwargs):
    return Character(classs=CLASSES["rogue"], **kwargs)


def Sorcerer(**kwargs):
    return Character(classs=CLASSES["sorcerer"], **kwargs)


def Warlock(**kwargs):
    return Character(classs=CLASSES["warlock"], **kwargs)


def Wizard(**kwargs):
    return Character(classs=CLASSES["wizard"], **kwargs)
