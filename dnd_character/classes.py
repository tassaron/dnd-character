from .SRD import SRD_classes as CLASSES
from .character import Character


def Barbarian(**kwargs) -> Character:
    return Character(classs=CLASSES["barbarian"], **kwargs)


def Bard(**kwargs) -> Character:
    return Character(classs=CLASSES["bard"], **kwargs)


def Cleric(**kwargs) -> Character:
    return Character(classs=CLASSES["cleric"], **kwargs)


def Druid(**kwargs) -> Character:
    return Character(classs=CLASSES["druid"], **kwargs)


def Fighter(**kwargs) -> Character:
    return Character(classs=CLASSES["fighter"], **kwargs)


def Monk(**kwargs) -> Character:
    return Character(classs=CLASSES["monk"], **kwargs)


def Paladin(**kwargs) -> Character:
    return Character(classs=CLASSES["paladin"], **kwargs)


def Ranger(**kwargs) -> Character:
    return Character(classs=CLASSES["ranger"], **kwargs)


def Rogue(**kwargs) -> Character:
    return Character(classs=CLASSES["rogue"], **kwargs)


def Sorcerer(**kwargs) -> Character:
    return Character(classs=CLASSES["sorcerer"], **kwargs)


def Warlock(**kwargs) -> Character:
    return Character(classs=CLASSES["warlock"], **kwargs)


def Wizard(**kwargs) -> Character:
    return Character(classs=CLASSES["wizard"], **kwargs)
