import pytest
from dnd_character import Character
from dnd_character.classes import CLASSES


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
def test_class_features_data_exist(input, expected_value):
    c = Character(**input)
    assert c.class_features_data == expected_value
