import pytest
from dnd_character import Character
from dnd_character.classes import CLASSES
from dnd_character.features import (
    get_class_features_data,
    reset_class_features_data_counters,
)
from dnd_character.experience import experience_at_level


@pytest.mark.parametrize(
    ("input", "expected_value"),
    (
        ({"level": 1}, None),
        (
            {"classs": CLASSES["barbarian"]},
            {
                "brutal_critical_dice": 0,
                "max_rage_count": 2,
                "available_rage_count": 2,
                "rage_damage_bonus": 2,
            },
        ),
        (
            {"classs": CLASSES["barbarian"], "level": 9},
            {
                "brutal_critical_dice": 1,
                "max_rage_count": 4,
                "available_rage_count": 4,
                "rage_damage_bonus": 3,
            },
        ),
        (
            {"classs": CLASSES["bard"], "level": 1, "charisma": 14},
            {
                "bardic_inspiration_die": 6,
                "magical_secrets_max_5": 0,
                "magical_secrets_max_7": 0,
                "magical_secrets_max_9": 0,
                "song_of_rest_die": 0,
                "max_inspiration_count": 2,
                "available_inspiration_count": 2,
            },
        ),
        (
            {"classs": CLASSES["wizard"], "level": 20},
            {
                "arcane_recovery_levels": 10,
                "max_arcane_recovery": 1,
                "available_arcane_recovery": 1,
                "days_since_last_arcane_recovery": 999,
            },
        ),
    ),
)
def test_class_features_data_exist_after_init(input, expected_value):
    c = Character(**input)
    assert c.class_features_data == expected_value


def test_reset_class_features_data_bard_level_1():
    c = Character(classs=CLASSES["bard"], level=1, charisma=10)
    # inspiration count should be 1 in this situation
    data = get_class_features_data(c)
    assert data["max_inspiration_count"] == 1
    data["available_inspiration_count"] = 0
    # at level 1 a short rest should NOT restore inspiration count
    data = reset_class_features_data_counters(
        character=c, data=data, short_rest=True, long_rest=False
    )
    assert data["available_inspiration_count"] == 0
    # a long rest should always restore inspiration count
    data = reset_class_features_data_counters(
        character=c, data=data, short_rest=False, long_rest=True
    )
    assert data["available_inspiration_count"] == 1


def test_reset_class_features_data_bard_level_5():
    c = Character(classs=CLASSES["bard"], level=5, charisma=10)
    # inspiration count should be 5 in this situation
    data = get_class_features_data(c)
    assert data["max_inspiration_count"] == 1
    data["available_inspiration_count"] = 0
    # at level 5 a short rest should restore inspiration count
    data = reset_class_features_data_counters(
        character=c, data=data, short_rest=True, long_rest=False
    )
    assert data["available_inspiration_count"] == 1


def test_class_features_data_monk_ki_points_level_1():
    c = Character(classs=CLASSES["monk"])
    assert c.class_features_data["max_ki_points"] == 0


def test_class_features_data_monk_ki_points_level_2_init():
    c = Character(classs=CLASSES["monk"], level=2)
    assert c.class_features_data["max_ki_points"] == 2


def test_class_features_data_monk_ki_points_level_2_init_experience():
    c = Character(classs=CLASSES["monk"], experience=experience_at_level(2))
    assert c.class_features_data["max_ki_points"] == 2


def test_class_features_data_monk_ki_points_level_increase_level():
    c = Character(classs=CLASSES["monk"])
    assert c.class_features_data["max_ki_points"] == 0
    c.level = 2
    assert c.class_features_data["max_ki_points"] == 2


def test_class_features_data_monk_ki_points_level_increase_experience():
    c = Character(classs=CLASSES["monk"])
    assert c.class_features_data["max_ki_points"] == 0
    assert c.class_features_data["available_ki_points"] == 0
    c.experience = experience_at_level(2)
    assert c.class_features_data["max_ki_points"] == 2
    # available counter stays at 0 after level up despite max increasing
    assert c.class_features_data["available_ki_points"] == 0
