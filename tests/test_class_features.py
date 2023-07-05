from dnd_character import Character
from dnd_character.classes import CLASSES
from dnd_character.experience import experience_at_level


def test_class_features_apply_experience_gain():
    bard = Character(classs=CLASSES["bard"])
    for i in range(0, experience_at_level(20), 100):
        bard.experience += 100
    assert len(bard.class_features) == 24


def test_class_features_apply_level_gain():
    bard = Character(classs=CLASSES["bard"])
    for i in range(20):
        bard.level += 1
    assert len(bard.class_features) == 24


def test_class_features_apply_experience_jump():
    bard = Character(classs=CLASSES["bard"])
    bard.experience = experience_at_level(20)
    assert len(bard.class_features) == 24


def test_class_features_apply_level_jump():
    bard = Character(classs=CLASSES["bard"])
    bard.level = 20
    assert len(bard.class_features) == 24


def test_class_features_apply_high_experience_initialized():
    bard = Character(classs=CLASSES["bard"], experience=experience_at_level(20))
    assert len(bard.class_features) == 24


def test_class_features_apply_high_level_initialized():
    bard = Character(classs=CLASSES["bard"], level=20)
    assert len(bard.class_features) == 24


def test_class_features_regenerated_if_none():
    bard = Character(classs=CLASSES["bard"])
    bard.class_features = None
    new_bard = Character(**dict(bard))
    assert len(new_bard.class_features) == 2


def test_classless_class_features_regenerated_if_none():
    char = Character()
    char.class_features = None
    new_char = Character(**dict(char))
    assert len(new_char.class_features) == 0
