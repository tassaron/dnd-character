from typing import Optional
from dataclasses import dataclass
from .SRD import SRD_classes
from .character import Character


@dataclass(kw_only=True, frozen=True, slots=True)
class _CLASS:
    index: str
    name: str
    url: str
    hit_die: int
    saving_throws: list[dict[str, str]]
    class_levels: dict
    subclasses: list[dict]
    multi_classing: dict
    proficiencies: list[dict[str, str]]
    proficiency_choices: list[dict]
    starting_equipment: list[dict]
    starting_equipment_options: list[dict]
    spellcasting: Optional[dict] = None
    spells: Optional[str] = None


CLASSES = {
    class_index: _CLASS(**class_data) for class_index, class_data in SRD_classes.items()
}


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
