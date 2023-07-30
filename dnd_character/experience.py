"""
An integer-like property of the Character object that handles everything related to experience:
experience points, leveling up and down, etc.
"""
from functools import lru_cache
from typing import TYPE_CHECKING
import logging


if TYPE_CHECKING:
    # allows type annotations to work without a circular import
    # https://peps.python.org/pep-0563/
    from .character import Character as Character


LOG = logging.getLogger(__package__)


class Experience:
    def __init__(self, character: "Character", experience: int):
        # this typically occurs while `character` is partially initialized (during __init__)
        self.character = character
        self._experience = experience
        self.character.level = level_at_experience(experience)

    @property
    def experience(self) -> "Experience":
        return self

    @experience.setter
    def experience(self, new_val: int) -> None:
        self._experience = new_val
        self.update_level()

    def update_level(self) -> None:
        self.character.level = level_at_experience(self._experience)

    def __eq__(self, other: object) -> bool:
        if isinstance(object, type(self)):
            return self._experience == other._experience
        return self._experience == other

    def __add__(self, new_val: int) -> int:
        val = self._experience + int(new_val)
        return val if val >= 0 else 0

    def __sub__(self, new_val: int) -> int:
        val = self._experience - new_val
        return val if val >= 0 else 0

    def __str__(self) -> str:
        return str(self._experience)

    def __int__(self) -> int:
        return self._experience

    @property
    def to_next_level(self) -> int:
        """
        Returns experience remaining until next level is reached
        """
        if self.character.level != level_at_experience(self._experience):
            LOG.warning(
                f"{str(self.character.name)} has a custom level: {str(self.character.level)}"
                f" which means to_next_level returned 0"
            )
            return 0
        try:
            return level_progression[self.character.level + 1] - self._experience
        except IndexError:
            return 0

    @property
    def to_last_level(self) -> int:
        """
        Returns experience remaining (to subtract) until previous level is reached
        """
        if self.character.level != level_at_experience(self._experience):
            LOG.warning(
                f"{str(self.character.name)} has a custom level: {str(self.character.level)}"
                f" which means to_last_level returned 0"
            )
            return 0
        return self._experience - level_progression[self.character.level]


@lru_cache(maxsize=None)
def level_at_experience(num: int) -> int:
    for level, threshold in enumerate(level_progression):
        if num >= threshold:
            continue
        return level - 1
    return 20


def experience_at_level(num: int) -> int:
    return level_progression[num]


level_progression = [
    0,
    0,
    300,
    900,
    2700,
    6500,  # 5
    14000,
    23000,
    34000,
    48000,
    64000,  # 10
    85000,
    100000,
    120000,
    140000,
    165000,  # 15
    195000,
    225000,
    265000,
    305000,
    355000,  # 20
]
