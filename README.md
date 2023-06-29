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
The `classes` module has functions for creating all 12 classes from the System Reference Document. The `monsters` module has a dictionary of monsters, which are dictionaries themselves.
```
from dnd_character.classes import Bard
from dnd_character.monsters import SRD_monsters
from random import randint

brianna = Bard(
    name="Brianna",
    level=10,
    )
zombie = SRD_monsters["zombie"]
attack_bonus = zombie["actions"][0]["attack_bonus"]
# Zombie rolls a d20 to attack a Bard
if randint(1, 20) + attack_bonus >= brianna.armor_class:
    print(f"{brianna.name} was hit by {zombie['name']}!")
else:
    print(f"{brianna.name} bravely dodged the attack")
```

### Leveling and Experience
The library should help leveling up characters automatically if you manage the Character's `experience` attribute. It's simpler to avoid modifying the level directly.
```
import dnd_character
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
```
from dnd_character.classes import Paladin
from pprint import pprint
sturm = Paladin(dexterity=10)
pprint(sturm.inventory)
print(sturm.armor_class)
# Remove Chain Mail
sturm.removeItem(sturm.inventory[0])
print(sturm.armor_class)
# New Item
from dnd_character.equipment import SRD_equipment
dragonlance = SRD_equipment['lance']
dragonlance["name"] = "Dragonlance®"
sturm.giveItem(dragonlance)
# View optional starting equipment
pprint(sturm.player_options)
```


### Using Spells
Support for spells is not super great at the moment. Characters have dictionaries like `spells_known` and `cantrips_known` in which you're expected to store dictionaries from `SRD_spells`... but there's no useful help from the library here. Yet!
```
from dnd_character.spellcasting import SRD_spells, spells_for_class_level
from pprint import pprint
cantrips = spells_for_class_level('wizard', 0)
print(f"Cantrips available to a Wizard: {', '.join(cantrips)}")
for spell in cantrips:
    print(f"{SRD_spells[spell]['name']}:")
    pprint(SRD_spells[spell])
    break
```


## Character Object
Normal initialization arguments for a Character object:
```
name         (str)
age          (str)
gender       (str)
alignment    (str): character's two letter alignment
description  (str): physical description of player character
biography    (str): backstory of player character	
level        (int): starting level
wealth       (int): starting wealth	
strength     (int)
dexterity    (int)
constitution (int)
wisdom       (int)
intelligence (int)
charisma     (int)
hp           (int):
classs      (dict): JSON returned from the 5e API -- dnd_character.SRD.SRD_classes["bard"]
```
In addition, the Character object can receive attributes that are normally set automatically, such as the UUID. This is for re-loading the objects from serialized data (via `Character(**characterData)`) and probably aren't arguments you would write manually into your code.


## Contributing
Please feel free to open a Pull Request on GitHub! I would be happy to help merge any contributions no matter your skill level.
