from dnd_character.monsters import Monster, SRD_monsters


def test_zombie():
    zombie = Monster("zombie")
    expected_zombie = {
        "index": "zombie",
        "url": "/api/monsters/zombie",
        "name": "Zombie",
        "size": "Medium",
        "type": "undead",
        "subtype": None,
        "alignment": "neutral evil",
        "hit_points": 22,
        "hit_dice": "3d8",
        "hit_points_roll": "3d8+9",
        "strength": 13,
        "dexterity": 6,
        "constitution": 16,
        "intelligence": 3,
        "wisdom": 6,
        "charisma": 5,
    }
    serialized_zombie = dict(zombie)
    assert all([serialized_zombie[k] == v for k, v in expected_zombie.items()])


def test_all_monsters():
    """Constructs all 334 monsters from the SRD - how scary!"""
    for monster in SRD_monsters:
        assert Monster(monster).name == SRD_monsters[monster]["name"]
