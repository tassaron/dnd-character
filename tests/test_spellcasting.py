from dnd_character.spellcasting import spells_for_class_level


def test_cantrips_wizard():
    expected_cantrips = [
        "prestidigitation",
        "true-strike",
        "message",
        "light",
        "fire-bolt",
        "ray-of-frost",
        "minor-illusion",
        "chill-touch",
        "mending",
        "dancing-lights",
        "poison-spray",
        "shocking-grasp",
        "acid-splash",
        "mage-hand",
    ]
    assert sorted(spells_for_class_level("wizard", 0)) == sorted(expected_cantrips)
