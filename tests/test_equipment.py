from ast import literal_eval
import pytest
from dnd_character.equipment import Item, SRD_equipment


def test_all_items_instantiation():
    """Constructs all 237 monsters from the SRD - we are now encumbered"""
    for item in SRD_equipment:
        assert Item(item).name == SRD_equipment[item]["name"]


# Run the item serialization test with 7 different items
@pytest.mark.parametrize(
    ("item_name", "expected_value"),
    (
        (
            "alchemists-supplies",
            {
                "contents": [],
                "cost": {"quantity": 50, "unit": "gp"},
                "desc": [
                    "These special tools include the items needed to pursue a craft or "
                    "trade. The table shows examples of the most common types of tools, "
                    "each providing items related to a single craft. Proficiency with a "
                    "set of artisan's tools lets you add your proficiency bonus to any "
                    "ability checks you make using the tools in your craft. Each type of "
                    "artisan's tools requires a separate proficiency."
                ],
                "equipment_category": {
                    "index": "tools",
                    "name": "Tools",
                    "url": "/api/equipment-categories/tools",
                },
                "index": "alchemists-supplies",
                "name": "Alchemist's Supplies",
                "properties": [],
                "special": [],
                "tool_category": "Artisan's Tools",
                "url": "/api/equipment/alchemists-supplies",
                "weight": 8,
            },
        ),
        (
            "dagger",
            {
                "category_range": "Simple Melee",
                "contents": [],
                "cost": {"quantity": 2, "unit": "gp"},
                "damage": {
                    "damage_dice": "1d4",
                    "damage_type": {
                        "index": "piercing",
                        "name": "Piercing",
                        "url": "/api/damage-types/piercing",
                    },
                },
                "desc": [],
                "equipment_category": {
                    "index": "weapon",
                    "name": "Weapon",
                    "url": "/api/equipment-categories/weapon",
                },
                "index": "dagger",
                "name": "Dagger",
                "properties": [
                    {
                        "index": "finesse",
                        "name": "Finesse",
                        "url": "/api/weapon-properties/finesse",
                    },
                    {
                        "index": "light",
                        "name": "Light",
                        "url": "/api/weapon-properties/light",
                    },
                    {
                        "index": "thrown",
                        "name": "Thrown",
                        "url": "/api/weapon-properties/thrown",
                    },
                    {
                        "index": "monk",
                        "name": "Monk",
                        "url": "/api/weapon-properties/monk",
                    },
                ],
                "range": {"normal": 5},
                "special": [],
                "throw_range": {"long": 60, "normal": 20},
                "url": "/api/equipment/dagger",
                "weapon_category": "Simple",
                "weapon_range": "Melee",
                "weight": 1,
            },
        ),
        (
            "battleaxe",
            {
                "category_range": "Martial Melee",
                "contents": [],
                "cost": {"quantity": 10, "unit": "gp"},
                "damage": {
                    "damage_dice": "1d8",
                    "damage_type": {
                        "index": "slashing",
                        "name": "Slashing",
                        "url": "/api/damage-types/slashing",
                    },
                },
                "desc": [],
                "equipment_category": {
                    "index": "weapon",
                    "name": "Weapon",
                    "url": "/api/equipment-categories/weapon",
                },
                "index": "battleaxe",
                "name": "Battleaxe",
                "properties": [
                    {
                        "index": "versatile",
                        "name": "Versatile",
                        "url": "/api/weapon-properties/versatile",
                    }
                ],
                "range": {"normal": 5},
                "special": [],
                "two_handed_damage": {
                    "damage_dice": "1d10",
                    "damage_type": {
                        "index": "slashing",
                        "name": "Slashing",
                        "url": "/api/damage-types/slashing",
                    },
                },
                "url": "/api/equipment/battleaxe",
                "weapon_category": "Martial",
                "weapon_range": "Melee",
                "weight": 4,
            },
        ),
        (
            "arrow",
            {
                "contents": [],
                "cost": {"quantity": 1, "unit": "gp"},
                "desc": [],
                "equipment_category": {
                    "index": "adventuring-gear",
                    "name": "Adventuring Gear",
                    "url": "/api/equipment-categories/adventuring-gear",
                },
                "gear_category": {
                    "index": "ammunition",
                    "name": "Ammunition",
                    "url": "/api/equipment-categories/ammunition",
                },
                "index": "arrow",
                "name": "Arrow",
                "properties": [],
                "quantity": 20,
                "special": [],
                "url": "/api/equipment/arrow",
                "weight": 1,
            },
        ),
        (
            "burglars-pack",
            {
                "contents": [
                    {
                        "item": {
                            "index": "backpack",
                            "name": "Backpack",
                            "url": "/api/equipment/backpack",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "ball-bearings-bag-of-1000",
                            "name": "Ball bearings (bag of 1,000)",
                            "url": "/api/equipment/ball-bearings-bag-of-1000",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "string-10-feet",
                            "name": "String (10 feet)",
                            "url": "/api/equipment/string-10-feet",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "bell",
                            "name": "Bell",
                            "url": "/api/equipment/bell",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "candle",
                            "name": "Candle",
                            "url": "/api/equipment/candle",
                        },
                        "quantity": 5,
                    },
                    {
                        "item": {
                            "index": "crowbar",
                            "name": "Crowbar",
                            "url": "/api/equipment/crowbar",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "hammer",
                            "name": "Hammer",
                            "url": "/api/equipment/hammer",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "piton",
                            "name": "Piton",
                            "url": "/api/equipment/piton",
                        },
                        "quantity": 10,
                    },
                    {
                        "item": {
                            "index": "lantern-hooded",
                            "name": "Lantern, hooded",
                            "url": "/api/equipment/lantern-hooded",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "oil-flask",
                            "name": "Oil (flask)",
                            "url": "/api/equipment/oil-flask",
                        },
                        "quantity": 2,
                    },
                    {
                        "item": {
                            "index": "rations-1-day",
                            "name": "Rations (1 day)",
                            "url": "/api/equipment/rations-1-day",
                        },
                        "quantity": 5,
                    },
                    {
                        "item": {
                            "index": "tinderbox",
                            "name": "Tinderbox",
                            "url": "/api/equipment/tinderbox",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "waterskin",
                            "name": "Waterskin",
                            "url": "/api/equipment/waterskin",
                        },
                        "quantity": 1,
                    },
                    {
                        "item": {
                            "index": "rope-hempen-50-feet",
                            "name": "Rope, hempen (50 feet)",
                            "url": "/api/equipment/rope-hempen-50-feet",
                        },
                        "quantity": 1,
                    },
                ],
                "cost": {"quantity": 16, "unit": "gp"},
                "desc": [],
                "equipment_category": {
                    "index": "adventuring-gear",
                    "name": "Adventuring Gear",
                    "url": "/api/equipment-categories/adventuring-gear",
                },
                "gear_category": {
                    "index": "equipment-packs",
                    "name": "Equipment Packs",
                    "url": "/api/equipment-categories/equipment-packs",
                },
                "index": "burglars-pack",
                "name": "Burglar's Pack",
                "properties": [],
                "special": [],
                "url": "/api/equipment/burglars-pack",
            },
        ),
        (
            "animal-feed-1-day",
            {
                "contents": [],
                "cost": {"quantity": 5, "unit": "cp"},
                "desc": [],
                "equipment_category": {
                    "index": "mounts-and-vehicles",
                    "name": "Mounts and Vehicles",
                    "url": "/api/equipment-categories/mounts-and-vehicles",
                },
                "index": "animal-feed-1-day",
                "name": "Animal Feed (1 day)",
                "properties": [],
                "special": [],
                "url": "/api/equipment/animal-feed-1-day",
                "vehicle_category": "Tack, Harness, and Drawn Vehicles",
                "weight": 10,
            },
        ),
        (
            "camel",
            {
                "capacity": "480 lb.",
                "contents": [],
                "cost": {"quantity": 50, "unit": "gp"},
                "desc": [],
                "equipment_category": {
                    "index": "mounts-and-vehicles",
                    "name": "Mounts and Vehicles",
                    "url": "/api/equipment-categories/mounts-and-vehicles",
                },
                "index": "camel",
                "name": "Camel",
                "properties": [],
                "special": [],
                "speed": {"quantity": 50, "unit": "ft/round"},
                "url": "/api/equipment/camel",
                "vehicle_category": "Mounts and Other Animals",
            },
        ),
    ),
)
def test_item_serialization(item_name: str, expected_value: dict):
    item = Item(item_name)
    serialized_item = literal_eval(str(dict(item)))
    assert all([serialized_item[k] == v for k, v in expected_value.items()])
