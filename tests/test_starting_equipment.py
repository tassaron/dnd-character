from ast import literal_eval
from dnd_character.classes import *


def test_player_options_barbarian():
    assert Barbarian().player_options["starting_equipment"] == [
        "choose from 1 x Greataxe, 1 x Martial Melee Weapons (choice from Battleaxe, Flail, "
        "Glaive, Greataxe, Greatsword, Halberd, Lance, Longsword, Maul, Morningstar, Pike, "
        "Rapier, Scimitar, Shortsword, Trident, War pick, Warhammer, Whip)",
        "choose from 2 x Handaxe, 1 x Simple Weapons (choice from Club, Dagger, Greatclub, "
        "Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, "
        "Dart, Shortbow, Sling)",
    ]


def test_player_options_bard():
    assert Bard().player_options["starting_equipment"] == [
        "choose from 1 x Rapier, 1 x Longsword, 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Diplomat's Pack, 1 x Entertainer's Pack",
        "choose from 1 x Lute, 1 x Musical Instruments (choice from Bagpipes, Drum, Dulcimer, Flute, Lute, Lyre, Horn, Pan flute, Shawm, Viol)",
    ]


def test_player_options_cleric():
    assert Cleric().player_options["starting_equipment"] == [
        "choose from 1 x Mace, 1 x Warhammer",
        "choose from 1 x Scale Mail, 1 x Leather Armor, 1 x Chain Mail",
        "1 Crossbow, light, 20 Crossbow bolt",
        "choose from 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Priest's Pack, 1 x Explorer's Pack",
        "Holy Symbols (choice from Amulet, Emblem, Reliquary)",
    ]


def test_player_options_druid():
    assert Druid().player_options["starting_equipment"] == [
        "choose from 1 x Shield, 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Scimitar, 1 x Simple Melee Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear)",
        "Druidic Foci (choice from Sprig of mistletoe, Totem, Wooden staff, Yew wand)",
    ]


def test_player_options_fighter():
    assert Fighter().player_options["starting_equipment"] == [
        "1 Leather Armor, 1 Longbow, 20 Arrow",
        "choose from 1 x Chain Mail",
        "choose 1 from Martial Weapons (choice from Battleaxe, Flail, Glaive, Greataxe, Greatsword, Halberd, Lance, Longsword, Maul, Morningstar, Pike, Rapier, Scimitar, Shortsword, Trident, War pick, Warhammer, Whip, Blowgun, Crossbow, hand, Crossbow, heavy, Longbow, Net) or a Shield",
        "choose from 2 x Martial Weapons (choice from Battleaxe, Flail, Glaive, Greataxe, Greatsword, Halberd, Lance, Longsword, Maul, Morningstar, Pike, Rapier, Scimitar, Shortsword, Trident, War pick, Warhammer, Whip, Blowgun, Crossbow, hand, Crossbow, heavy, Longbow, Net)",
        "1 Crossbow, light, 20 Crossbow bolt",
        "choose from 2 x Handaxe",
        "choose from 1 x Dungeoneer's Pack, 1 x Explorer's Pack",
    ]


def test_starting_equipment_monk():
    inv = dict(Monk())["inventory"]
    assert inv[0]["index"] == "dart" and inv[0]["quantity"] == 10


def test_starting_equipment_monk_serialized():
    inv = dict(Character(**literal_eval(str(dict(Monk())))))["inventory"]
    assert inv[0]["index"] == "dart" and inv[0]["quantity"] == 10


def test_player_options_monk():
    assert Monk().player_options["starting_equipment"] == [
        "choose from 1 x Shortsword, 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Dungeoneer's Pack, 1 x Explorer's Pack",
    ]


def test_player_options_paladin():
    assert Paladin().player_options["starting_equipment"] == [
        "choose 1 from Martial Weapons (choice from Battleaxe, Flail, Glaive, Greataxe, Greatsword, Halberd, Lance, Longsword, Maul, Morningstar, Pike, Rapier, Scimitar, Shortsword, Trident, War pick, Warhammer, Whip, Blowgun, Crossbow, hand, Crossbow, heavy, Longbow, Net) or a Shield",
        "choose from 2 x Martial Weapons (choice from Battleaxe, Flail, Glaive, Greataxe, Greatsword, Halberd, Lance, Longsword, Maul, Morningstar, Pike, Rapier, Scimitar, Shortsword, Trident, War pick, Warhammer, Whip, Blowgun, Crossbow, hand, Crossbow, heavy, Longbow, Net)",
        "choose from 5 x Javelin, 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Priest's Pack, 1 x Explorer's Pack",
        "Holy Symbols (choice from Amulet, Emblem, Reliquary)",
    ]


def test_player_options_ranger():
    assert Ranger().player_options["starting_equipment"] == [
        "choose from 1 x Scale Mail, 1 x Leather Armor",
        "choose from 2 x Shortsword, 2 x Simple Melee Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear)",
        "choose from 1 x Dungeoneer's Pack, 1 x Explorer's Pack",
    ]


def test_player_options_rogue():
    assert Rogue().player_options["starting_equipment"] == [
        "choose from 1 x Rapier, 1 x Shortsword",
        "1 Shortbow, 20 Arrow",
        "choose from 1 x Shortsword",
        "choose from 1 x Burglar's Pack, 1 x Dungeoneer's Pack, 1 x Explorer's Pack",
    ]


def test_player_options_sorcerer():
    assert Sorcerer().player_options["starting_equipment"] == [
        "1 Crossbow, light, 20 Crossbow bolt",
        "choose from 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Component pouch, 1 x Arcane Foci (choice from Crystal, Orb, Rod, Staff, Wand)",
        "choose from 1 x Dungeoneer's Pack, 1 x Explorer's Pack",
    ]


def test_player_options_warlock():
    assert Warlock().player_options["starting_equipment"] == [
        "1 Crossbow, light, 20 Crossbow bolt",
        "choose from 1 x Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
        "choose from 1 x Component pouch, 1 x Arcane Foci (choice from Crystal, Orb, Rod, Staff, Wand)",
        "choose from 1 x Scholar's Pack, 1 x Dungeoneer's Pack",
        "Simple Weapons (choice from Club, Dagger, Greatclub, Handaxe, Javelin, Light hammer, Mace, Quarterstaff, Sickle, Spear, Crossbow, light, Dart, Shortbow, Sling)",
    ]


def test_player_options_wizard():
    assert Wizard().player_options["starting_equipment"] == [
        "choose from 1 x Quarterstaff, 1 x Dagger",
        "choose from 1 x Component pouch, 1 x Arcane Foci (choice from Crystal, Orb, Rod, Staff, Wand)",
        "choose from 1 x Scholar's Pack, 1 x Explorer's Pack",
    ]
