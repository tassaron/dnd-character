from dnd_character import Character
from dnd_character.classes import CLASSES
from dnd_character.experience import experience_at_level


def test_class_features_apply_experience_gain():
    bard = Character(classs=CLASSES["bard"])
    for i in range(0, experience_at_level(20), 100):
        bard.experience += 100
    assert len(bard.class_features) == 26


def test_class_features_apply_level_gain():
    bard = Character(classs=CLASSES["bard"])
    for i in range(20):
        bard.level += 1
    assert len(bard.class_features) == 26


def test_class_features_apply_experience_jump():
    bard = Character(classs=CLASSES["bard"])
    bard.experience = experience_at_level(20)
    assert len(bard.class_features) == 26


def test_class_features_apply_level_jump():
    bard = Character(classs=CLASSES["bard"])
    bard.level = 20
    assert len(bard.class_features) == 26


def test_class_features_apply_high_experience_initialized():
    bard = Character(classs=CLASSES["bard"], experience=experience_at_level(20))
    assert len(bard.class_features) == 26


def test_class_features_apply_high_level_initialized():
    bard = Character(classs=CLASSES["bard"], level=20)
    assert len(bard.class_features) == 26
