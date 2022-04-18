from dnd_character import Character
from dnd_character.experience import experience_at_level, Experience


def twenty_levels_of_character():
    """
    A generator that yields the same character 20 times at levels 1-20
    """
    char = Character()
    i = 1
    while i < 21:
        char.experience = experience_at_level(i)
        yield char
        i += 1


def twenty_levels_of_characters():
    """
    A generator that yields 20 characters at levels 1-20
    """
    i = 1
    while i < 21:
        yield Character(level=i)
        i += 1


def test_experience_thresholds_newly_initialized():
    for i, character in enumerate(twenty_levels_of_characters()):
        assert character.experience == experience_at_level(i + 1)


def test_experience_thresholds_already_initialized():
    for i, character in enumerate(twenty_levels_of_character()):
        assert character.experience == experience_at_level(i + 1)


def test_leveling_down():
    character = Character(level=2)
    assert character.level == 2
    character.experience -= 1
    assert character.level == 1


def test_leveling_up():
    character = Character(experience=experience_at_level(2) - 1)
    assert character.level == 1
    character.experience += 1
    assert character.level == 2


def test_custom_level_number_initialized():
    character = Character(level=3, experience=experience_at_level(2) - 1)
    assert character.level == 3 and character.experience == experience_at_level(2) - 1


def test_custom_level_number_overwritten():
    character = Character(level=3, experience=experience_at_level(2) - 1)
    character.experience = character.experience + 1
    assert character.level == 2


def test_custom_level_has_no_progression():
    character = Character(level=3, experience=experience_at_level(2) - 1)
    assert character.experience.to_next_level == 0


def test_level_19():
    character = Character(level=19)
    assert character.experience.to_next_level == 50000


def test_maximum_level():
    character = Character(level=20)
    assert character.experience.to_next_level == 0


def test_no_negative_experience():
    character = Character(experience=100)
    character.experience -= 101
    assert character.experience == 0


def test_experience_setter_none():
    character = Character(experience=100)
    character.experience = None
    assert character.experience == 100


def test_experience_setter_object():
    character = Character(experience=100)
    experience = Experience(character, 200)
    character.experience = experience
    assert character.experience == 200
