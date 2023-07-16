from dnd_character import Character, Bard
from dnd_character.equipment import SRD_equipment


def test_remove_shields():
    t = Character()
    t.giveItem(SRD_equipment["shield"])
    t.removeShields()
    # only non-shields should exist in the armor category
    assert not [
        item
        for item in t.inventory
        if item["equipment_category"]["index"] == "armor"
        and item["armor_category"] == "Shield"
    ]


def test_shield_increases_armor_class():
    # shield equipment gives +2 AC
    t = Character(dexterity=10)
    t.giveItem(SRD_equipment["shield"])
    assert t.armor_class == 12
    t.removeItem(SRD_equipment["shield"])
    assert t.armor_class == 10


def test_remove_armor():
    t = Bard(dexterity=10)
    # Bard starts with armor which should be removed by this method
    t.removeArmor()
    assert not [
        item
        for item in t.inventory
        if item["equipment_category"]["index"] == "armor"
        and item["armor_category"] != "Shield"
    ]


def test_removing_shield_does_not_affect_equipped_armor():
    t = Bard(dexterity=14)
    t.giveItem(SRD_equipment["shield"])
    t.removeItem(SRD_equipment["shield"])
    assert t.armor_class == 13


def test_removing_armor_does_not_affect_equipped_shield():
    t = Bard(dexterity=10)
    t.giveItem(SRD_equipment["shield"])
    t.removeItem(SRD_equipment["leather-armor"])
    assert t.armor_class == 12
