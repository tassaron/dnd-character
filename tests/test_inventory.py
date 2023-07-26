from dnd_character import Character, Bard
from dnd_character.equipment import SRD_equipment, Item


def test_remove_shields():
    t = Character()
    t.give_item(Item("shield"))
    t.remove_shields()
    # only non-shields should exist in the armor category
    assert not [
        item
        for item in t.inventory
        if item.equipment_category["index"] == "armor"
        and item.armor_category == "Shield"
    ]


def test_shield_increases_armor_class():
    # shield equipment gives +2 AC
    t = Character(dexterity=10)
    shield = Item("shield")
    t.give_item(shield)
    assert t.armor_class == 12
    t.remove_item(shield)
    assert t.armor_class == 10


def test_remove_armor():
    t = Bard(dexterity=10)
    # Bard starts with armor which should be removed by this method
    t.remove_armor()
    assert not [
        item
        for item in t.inventory
        if item.equipment_category["index"] == "armor"
        and item.armor_category != "Shield"
    ]


def test_removing_shield_does_not_affect_equipped_armor():
    t = Bard(dexterity=14)
    shield = Item("shield")
    t.give_item(shield)
    t.remove_item(shield)
    assert t.armor_class == 13


def test_removing_armor_does_not_affect_equipped_shield():
    t = Bard(dexterity=10)
    t.give_item(Item("shield"))
    for item in t.inventory:
        if item.index == "leather-armor":
            t.remove_item(item)
    assert t.armor_class == 12
