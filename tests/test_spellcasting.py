import pytest
from ast import literal_eval
from dnd_character.character import Character
from dnd_character.classes import CLASSES, Bard, Wizard, Ranger
from dnd_character.spellcasting import spells_for_class_level, SPELLS, _SPELL


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
    for spell in SPELLS.values():
        assert _SPELL(**literal_eval(str(dict(spell)))) == spell


def test_cantrips_known_serializes_in_character():
    bard = Bard()
    bard.cantrips_known.append(SPELLS["thunderwave"])
    assert (
        bard.cantrips_known[0].index
        == literal_eval(str(dict(bard)))["cantrips_known"][0]["index"]
    )


def test_spells_known_serializes_in_character():
    bard = Bard()
    bard.spells_known.append(SPELLS["thunderwave"])
    assert (
        bard.spells_known[0].index
        == literal_eval(str(dict(bard)))["spells_known"][0]["index"]
    )


def test_spells_prepared_serializes_in_character():
    wiz = Wizard()
    wiz.spells_prepared.append(SPELLS["fireball"])
    assert (
        wiz.spells_prepared[0].index
        == literal_eval(str(dict(wiz)))["spells_prepared"][0]["index"]
    )


@pytest.mark.parametrize(
    ("class_index", "level", "expected"),
    (("bard", 2, 5), ("warlock", 10, 10), ("ranger", 4, 3)),
)
def test_spells_known_maximum(class_index, level, expected):
    c = Character(classs=CLASSES[class_index], level=level)
    assert c.spells_known.maximum == expected


def test_spells_prepared_maximum_cleric():
    c = Character(classs=CLASSES["cleric"], wisdom=14)
    assert c.spells_prepared.maximum == 3


def test_spells_prepared_maximum_wizard():
    c = Character(classs=CLASSES["wizard"], intelligence=14)
    assert c.spells_prepared.maximum == 3


def test_spells_exceeded_assignment():
    c = Character(classs=CLASSES["bard"])
    c.spells_known = [SPELLS["thunderwave"]] * 4
    assert c.spells_known.maximum == 4
    assert len(c.spells_known) == 4
    with pytest.raises(ValueError, match=" spells "):
        c.spells_known += [SPELLS["identify"]]


def test_spells_exceeded_append():
    c = Character(classs=CLASSES["bard"])
    c.spells_known = [SPELLS["thunderwave"]] * 4
    assert c.spells_known.maximum == 4
    assert len(c.spells_known) == 4
    with pytest.raises(ValueError, match=" spells "):
        c.spells_known.append(SPELLS["identify"])


def test_spells_exceeded_at_init():
    c = Character(classs=CLASSES["bard"], spells_known=[SPELLS["thunderwave"]] * 4)
    c_as_dict = dict(c)
    # add illegal spell while character is a dictionary
    c_as_dict["spells_known"].append(c_as_dict["spells_known"][0].copy())
    new_c = Character(**c_as_dict)
    # illegal spell increases maximum in this edge case - desireable? I think so
    assert len(new_c.spells_known) == new_c.spells_known.maximum
