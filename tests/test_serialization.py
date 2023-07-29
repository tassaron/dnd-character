from dnd_character import Character, Bard, Monk, CLASSES
from dnd_character.equipment import Item
from ast import literal_eval
import json


def test_character_repr():
    char = Character(experience=200, name="Grace")
    new_char = eval(repr(char))
    assert new_char == char


def test_character_dunder_eq_with_dict():
    char = Character(experience=200, name="Grace")
    assert char == dict(char)


def test_save_and_load_lvl1_character():
    player = Character()
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_character():
    player = Character(level=3)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl1_bard():
    player = Character(classs=CLASSES["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_bard():
    player = Character(level=3, classs=CLASSES["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_custom_lvl_character():
    player = Character(level=3, experience=100, constitution=10)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_experience():
    player = Character(experience=100)
    clone = Character(**dict(player))
    assert player._experience._experience == clone._experience._experience
    assert player.experience.to_next_level == clone.experience.to_next_level


def test_save_and_load_leveled_up_character():
    player = Character(classs=CLASSES["bard"])
    for i in range(900):
        player.experience += 1
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_literal_eval_constructs_valid_dict():
    char = Character(experience=200)
    assert literal_eval(str(dict(char))) == dict(char)


def test_literal_eval_constructs_valid_inventory():
    char = Character()
    char.give_item(Item("burglars-pack"))
    char.give_item(Item("battleaxe"))
    char.give_item(Item("scale-mail"))
    assert literal_eval(str(dict(char))) == dict(char)


def test_property_decorated_methods_serialize():
    player = Character(experience=200, dexterity=15)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_hitpoints():
    player = Character()
    player.current_hp = 6
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_equipment():
    player = Character()
    player.give_item(Item("bagpipes"))
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_armor_class():
    player = Character(dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_light_armor_class():
    player = Character(classs=CLASSES["bard"], dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_heavy_armor_class():
    player = Character(classs=CLASSES["paladin"], dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_character_str():
    player = Character(classs=CLASSES["fighter"])
    player.give_item(Item("flute"))
    player.experience += 50
    character_repr = str(player)
    mandatory_attrs = [
        "name",
        "age",
        "gender",
        "description",
    ]
    assert sum(
        [
            f"{attr.title()}: {str(player.__dict__[attr])}" in character_repr
            for attr in mandatory_attrs
        ]
    ) == len(mandatory_attrs)
    assert f"Background:\n{str(player.background)}" in character_repr
    assert f"Class: {str(player.class_name)}" in character_repr
    assert f"Level: {str(player.level)}" in character_repr
    assert f"Experience: {str(player.experience)}" in character_repr
    assert (
        f"to next level: {str(player.experience.to_next_level)}"
        in character_repr.lower()
    )
    assert sum(
        [value["name"] in character_repr for value in player.proficiencies.values()]
    ) == len(player.proficiencies)
    assert sum([value.name in character_repr for value in player.inventory]) == len(
        player.inventory
    )
    assert sum(
        [value["name"] in character_repr for value in player.class_features.values()]
    ) == len(player.class_features)


def test_serialization_of_class_levels():
    bard = Bard(level=20)
    bard._class_levels = None
    serialized_bard = dict(bard)
    del serialized_bard["class_features"]
    new_bard = Character(**serialized_bard)
    # add _class_levels back onto old bard
    bard.classs = CLASSES["bard"]
    assert new_bard._class_levels == bard._class_levels
    assert new_bard.class_features == bard.class_features


def test_frightened_condition_serializes():
    bard = Bard(conditions={"frightened": True})
    serialized_bard = dict(bard)
    new_bard = Character(**serialized_bard)
    assert new_bard.conditions["frightened"] is True


def test_character_json_classless():
    c = Character(name="Canary")
    assert json.loads(json.dumps(dict(c))) == dict(c)


def test_character_json_monk_with_items():
    c = Monk()
    c.give_item(Item("dagger"))
    assert json.loads(json.dumps(dict(c))) == dict(c)
