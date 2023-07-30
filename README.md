# dnd-character

A Python library to make 5e Dungeons & Dragons characters for use in another app. Characters are serializable into Python dicts so they can be saved and loaded however you wish.

SRD rules are fetched from the [5e SRD API](https://github.com/5e-bits/5e-srd-api) the first time they're requested, then the JSON is cached locally for faster retrieval in the future. I've included the `json_cache` containing the SRD inside the repo in case this API changes, but when the API does change I will update this library. So please pin your version if you want to avoid any breaking changes.

You can use this library as a CLI tool to generate character sheets from the terminal; see `python -m dnd_character --help` for details.

## Installation and Use

1. Install from PyPI using `pip install dnd-character`
1. See `example.py` for example code on how to use the library.
1. Generate random character sheet text file with `python -m dnd_character --random > mycharactername.txt`

## Licenses

The software is EPL-2.0 and the text for this license is in `LICENSE` as is standard for software. Originally forked from [PyDnD](https://github.com/Coffee-fueled-deadlines/PyDnD). The contents of `dnd_character/json_cache` are retrieved from [5e-srd-api](https://github.com/5e-bits/5e-srd-api), and are covered by the Open Game License. See `dnd_character/json_cache/OGLv1.0a.txt` for details.

## Example Code

### Creating Characters and Monsters

The `classes` module has functions for creating all 12 classes from the System Reference Document. The `monsters` module has a factory function for creating monsters.

```python
from dnd_character.classes import Bard
from dnd_character.monsters import Monster
from random import randint

brianna = Bard(
    name="Brianna",
    level=10,
    )
zombie = Monster("zombie")
attack_bonus = zombie.actions[0]["attack_bonus"]
# Zombie rolls a d20 to attack a Bard
if randint(1, 20) + attack_bonus >= brianna.armor_class:
    print(f"{brianna.name} was hit by {zombie.name}!")
else:
    print(f"{brianna.name} bravely dodged the attack")
```

### Leveling and Experience

The library should help leveling up characters automatically if you manage the Character's `experience` attribute. It's simpler to avoid modifying the level directly.

```python
from dnd_character import Character
thor = Character(name="Thor")
assert thor.level == 1
thor.experience += 1000
assert thor.level == 3
assert thor.experience.to_next_level == 1700
thor.experience += thor.experience.to_next_level
assert thor.level == 4
```

### Starting Equipment

Characters initialized with a class will have the starting equipment of that class, and an attribute called `player_options` which lists the optional starting equipment.

```python
from dnd_character.classes import Paladin
from dnd_character.equipment import Item
from pprint import pprint
sturm = Paladin(dexterity=10)
pprint(sturm.inventory)
print(sturm.armor_class)
# Remove Chain Mail
sturm.remove_item(sturm.inventory[0])
print(sturm.armor_class)
# New Item
dragonlance = Item('lance')
dragonlance.name = "Dragonlance®"
sturm.give_item(dragonlance)
# View optional starting equipment
pprint(sturm.player_options)
```

### Using Spells

Spells are represented by _SPELL objects from `dnd_character.spellcasting`. The best way to find spells is using the `spells_for_class_level` function.

```python
from dnd_character.spellcasting import spells_for_class_level
cantrips = spells_for_class_level('wizard', 0)
print(f"Cantrips available to a Wizard:")
for spell in cantrips:
    print(spell)
```

Characters have lists to store _SPELL objects:

- `spells_prepared`
- `spells_known`
- `cantrips_known`

Characters have a `spell_slots` dictionary which shows the **total** spell slots. Depletion and rest mechanics are planned for a future version.

```python
from dnd_character import Wizard
from dnd_character.spellcasting import SPELLS
# Create wizard and teach Identify, a level 1 spell
my_wizard = Wizard(name="Gormwinkle")
my_wizard.spells_prepared.append(SPELLS["identify"])
# Get total spell slots
spell_slots_level_1 = my_wizard.spell_slots["spell_slots_level_1"]
print(f"{my_wizard.name} has {spell_slots_level_1} spell slots of 1st level")
# Cast until wizard runs out of spell slots
while spell_slots_level_1 > 0:
    print(f"Casting {SPELLS['identify'].name}!")
    spell_slots_level_1 -= 1
```

There is currently no way to manage wizard spellbooks or class-specific features such as the Wizard's arcane recovery or the Sorcerer's metamagic.

## Character Object

Normal initialization arguments for a Character object:

```text
name         (str)
age          (str)
gender       (str)
level        (int): starting level
hp           (int)
alignment    (str): character's two letter alignment (LE, CG, TN, etc.)
description  (str): physical description of player character
background   (str): one-word backstory (e.g., knight, chef, acolyte)
wealth       (int): if None, roll 4d10 for starting gp (gold pieces)
strength     (int): if None, roll 4d6 and drop the lowest
dexterity    (int): if None, roll 4d6 and drop the lowest
constitution (int): if None, roll 4d6 and drop the lowest
wisdom       (int): if None, roll 4d6 and drop the lowest
intelligence (int): if None, roll 4d6 and drop the lowest
charisma     (int): if None, roll 4d6 and drop the lowest
classs    (_CLASS): a D&D class object (e.g., CLASSES['bard'])
```

In addition, the Character object can receive attributes that are normally set automatically, such as the UUID. This is for re-loading the objects from serialized data (via `Character(**characterData)`) and probably aren't arguments you would write manually into your code.

## Serializing objects

All objects in this library can be turned into Python dicts, which can then be turned back into objects. This means characters (along with their items and spells), and monsters as well.

- `dict(object)` creates a serializable dict that could be reloaded from text (e.g., suitable for conversion to and from JSON)
- `repr(object)` prints a string that would re-construct the Python object if pasted into a REPL
- `str(object)` is not for serialization. It creates a "user-friendly" string

## Contributing

I greatly appreciate feedback about desired features and information about how you're using this library. Please feel free to open an issue or pull request on GitHub! I would be happy to help merge any contributions no matter your skill level.
