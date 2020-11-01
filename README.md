# dnd-character
A Python library to make 5e Dungeons & Dragons characters for use in another app. Characters are serializable into Python dicts so they can be saved and loaded however you wish.

SRD rules are fetched from the [5e SRD API](https://github.com/bagelbits/5e-srd-api) the first time they're requested, then the JSON is cached locally for faster retrieval in the future. I've included the `json_cache` containing the SRD inside the repo in case this API changes, but when the API does change I will update this library. So please pin your version if you want to avoid any breaking changes.


## Installation and Use
1. Install from PyPI using `pip install dnd-character`
1. See `example.py` for example code on how to use the library.


## Licenses
The software is EPL-2.0 and the text for this license is in `LICENSE` as is standard for software. Originally forked from [PyDnD](https://github.com/Coffee-fueled-deadlines/PyDnD). The contents of `dnd_character/json_cache` are retrieved from [5e-srd-api](https://github.com/bagelbits/5e-srd-api/issues/114), and are covered by the Open Game License. See `dnd_character/json_cache/OGLv1.0a.txt` for details.


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


## Leveling and Experience
The library should help leveling up characters automatically if simply manage the Character's `experience` attribute. It's better to avoid modifying the level directly.

### Example
```
>>> thor = Character(name="Thor")
>>> thor.experience += 1000
>>> thor.level
3
>>> thor.experience.to_next_level
1700
>>> thor.experience += thor.experience.to_next_level
>>> thor.level
4
```
