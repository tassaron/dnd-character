import logging
from typing import Union, Optional
from dataclasses import dataclass, asdict
from .SRD import SRD, SRD_endpoints, SRD_classes


LOG = logging.getLogger(__package__)
SRD_spells = {
    spell["index"]: SRD(spell["url"])
    for spell in SRD(SRD_endpoints["spells"])["results"]
}


@dataclass(kw_only=True, frozen=True, slots=True)
class _SPELL:
    """
    Dataclass for spells. Spells are suggested to be constants. (Immutable.)
    So deserialization shouldn't be necessary, but is possible with _SPELL(**dict).
    Or get the constant version from `dnd_character.spellcasting.SPELLS[spell_name]`
    """

    area_of_effect: Optional[dict[str, Union[str, int]]] = None
    attack_type: Optional[str] = None
    casting_time: str
    classes: list[dict[str, str]]
    components: list[str]
    concentration: bool
    damage: Optional[dict[str, dict[str, str]]] = None
    dc: Optional[dict[str, Union[str, dict[str, str]]]] = None
    desc: list[str]
    duration: str
    heal_at_slot_level: Optional[list[str]] = None
    higher_level: list[str]
    material: Optional[str] = None
    index: str
    level: int
    name: str
    range: str
    ritual: bool
    school: dict[str, str]
    subclasses: list[dict[str, str]]
    url: str

    def __iter__(self):
        me = asdict(self)
        for k, v in me.items():
            yield k, v


SPELLS: dict[str, _SPELL] = {
    index: _SPELL(**spell) for index, spell in SRD_spells.items()
}


class SpellList(list):
    """A list with a maximum size, for storing spells and cantrips"""

    def __init__(self, initial: Optional[list["_SPELL"]]) -> None:
        initial = initial if initial is not None else []
        self._maximum: int = len(initial)
        super().__init__(initial)

    @property
    def maximum(self) -> int:
        return self._maximum

    @maximum.setter
    def maximum(self, new_val: int) -> None:
        if len(self) > new_val:
            LOG.error("Too many spells in spell list to lower its maximum.")
            return
        self._maximum = new_val

    def append(self, new_val: "_SPELL") -> None:
        if len(self) + 1 > self.maximum:
            raise ValueError(f"Too many spells in list (max {self.maximum})")
        super().append(new_val)


spell_names_by_level = {
    i: [key for key, val in SRD_spells.items() if val["level"] == i] for i in range(10)
}

spell_names_by_class = {
    i: [
        key
        for key, val in SRD_spells.items()
        if i in (cindex["index"] for cindex in val["classes"])
    ]
    for i in SRD_classes.keys()
}


def spells_for_class_level(classs: str, level: int) -> set:
    if level > 9 or level < 0:
        raise ValueError("Spell levels only go from 0-9")
    return set(spell_names_by_class[classs]).intersection(
        set(spell_names_by_level[level])
    )
