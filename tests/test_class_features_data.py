import pytest
from dnd_character import Character


@pytest.mark.parametrize(
    ("input", "expected_value"),
    (
        ({"classs": CLASSES["barbarian"]}, None),
        ({"level": 1}, None),
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
                "max_arcane_recovery": 10,
                "available_arcane_recovery": 10,
                "days_since_last_arcane_recovery": 999,
            },
        ),
    ),
)
def test_class_features_data_exist(input, expected_value):
    c = Character(**input)
    assert c.class_features_data == expected_value
