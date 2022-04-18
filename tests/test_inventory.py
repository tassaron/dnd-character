from dnd_character import Character, Bard
from dnd_character.equipment import SRD_equipment


def test_remove_shields():
    t = Character()
    t.giveItem(SRD_equipment["shield"])
    t.removeShields()
    # only non-shields should exist in the armour category
    assert not [item for item in t.inventory if item["equipment_category"]["index"] == "armor" and item["armor_category"] == "Shield"]


def test_shield_increases_armour_class():
    # shield equipment gives +2 AC
    t = Character(dexterity=10)
    t.giveItem(SRD_equipment["shield"])
    assert t.armour_class == 12
    t.removeItem(SRD_equipment["shield"])
    assert t.armour_class == 10


def test_remove_armour():
    t = Bard(dexterity=10)
    # Bard starts with armour which should be removed by this method
    t.removeArmour()
    assert not [item for item in t.inventory if item["equipment_category"]["index"] == "armor" and item["armor_category"] != "Shield"]
