from dnd_character.classes import Wizard
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


def test_spell_slots_wizard():
    assert Wizard().spell_slots == {
        "cantrips_known": 3,
        "spell_slots_level_1": 2,
        "spell_slots_level_2": 0,
        "spell_slots_level_3": 0,
        "spell_slots_level_4": 0,
        "spell_slots_level_5": 0,
        "spell_slots_level_6": 0,
        "spell_slots_level_7": 0,
        "spell_slots_level_8": 0,
        "spell_slots_level_9": 0,
    }
