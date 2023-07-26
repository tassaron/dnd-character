from ast import literal_eval
from dnd_character.character import Character
from dnd_character.classes import Bard, Wizard, Ranger
from dnd_character.spellcasting import spells_for_class_level, SPELLS


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


def test_spell_slots_bard():
    assert Bard().spell_slots == {
        "cantrips_known": 2,
        "spells_known": 4,
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


def test_spell_slots_wizard():
    # wizard's class data is missing `spells_known`, which should receive the default of 0
    assert Wizard().spell_slots == {
        "cantrips_known": 3,
        "spells_known": 0,
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


def test_spell_slots_ranger():
    # ranger's class data is missing `cantrips_known` and all `spell_slots` > 5
    assert Ranger().spell_slots == {
        "cantrips_known": 0,
        "spells_known": 0,
        "spell_slots_level_1": 0,
        "spell_slots_level_2": 0,
        "spell_slots_level_3": 0,
        "spell_slots_level_4": 0,
        "spell_slots_level_5": 0,
        "spell_slots_level_6": 0,
        "spell_slots_level_7": 0,
        "spell_slots_level_8": 0,
        "spell_slots_level_9": 0,
    }


def test_spells_serialize():
    bard = Bard()
    bard.spells_known += SPELLS["thunderwave"]
    assert dict(Character(**literal_eval(str(dict(bard))))) == dict(bard)
