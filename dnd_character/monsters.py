from uuid import uuid4
from typing import Optional, Union
from dataclasses import dataclass, asdict
from .SRD import SRD_endpoints, SRD


SRD_monsters = {
    result["index"]: SRD(result["url"])
    for result in SRD(SRD_endpoints["monsters"])["results"]
}


@dataclass(kw_only=True)
class _Monster:
    index: str
    uid: str = uuid4().hex
    type: str
    subtype: Optional[str] = None
    desc: Optional[str] = None
    image: Optional[str] = None
    images: Optional[str] = None
    url: str
    name: str
    size: str
    alignment: str
    armor_class: list[dict[str, Union[str, int]]]
    hit_points: int
    hit_dice: str
    hit_points_roll: str
    speed: dict[str, str]
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    proficiencies: list[dict[str, Union[str, dict[str, str]]]]
    damage_vulnerabilities: list[str]
    damage_resistances: list[str]
    damage_immunities: list[str]
    condition_immunities: list[dict[str, str]]
    senses: dict[str, Union[str, int]]
    languages: str
    challenge_rating: float
    xp: int
    special_abilities: list[dict[str, str]]
    legendary_actions: list[dict[str, str]]
    actions: list[dict]
    reactions: Optional[list[dict]] = None
    forms: Optional[list[dict[str, str]]] = None

    def __iter__(self):
        me = asdict(self)
        for k, v in me.items():
            yield k, v


def Monster(index: str) -> _Monster:
    return _Monster(**SRD_monsters[index])
