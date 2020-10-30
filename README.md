# dnd-character
A Python library to make 5e Dungeons & Dragons characters for use in another app. Characters are serializable into Python dicts so they can be saved and loaded however you wish.

SRD rules are fetched from the [5e SRD API](https://github.com/bagelbits/5e-srd-api) the first time they're requested, then the JSON is cached locally for faster retrieval in the future. I've included the `json_cache` containing the SRD inside the repo in case this API changes, but when the API does change I will update this library. So please pin your version if you want to avoid any breaking changes.


# Installation
1. Install from PyPI using `pip install dnd-character`
1. See `example.py` for example code on how to use the library.


# Legalese
* The software is EPL-2.0 and the text for this license is in `LICENSE` as is standard for software. Originally forked from [PyDnD](https://github.com/Coffee-fueled-deadlines/PyDnD).
* The contents of `dnd_character/json_cache` are retrieved from [5e-srd-api](https://github.com/bagelbits/5e-srd-api/issues/114), and are covered by the Open Game License. See `dnd_character/json_cache/OGLv1.0a.txt` for details.


## Character Object
Normal initialization arguments for a Character object:
```
name         (str): Character character's name
age          (str): Character character's age
gender       (str): Character character's gender
alignment    (str): Character character's two letter alignment
description  (str): Physical description of player character
biography    (str): Backstory of player character	
level        (int): Character character's starting level
wealth       (int): Character character's starting wealth	
strength     (int): Character character's starting strength Ability Score
dexterity    (int): Character character's starting dexterity Ability Score
constitution (int): Character character's starting constitution Ability Score
wisdom       (int): Character character's starting wisdom Ability Score
intelligence (int): Character character's starting intelligence Ability Score
charisma     (int): Character character's starting charisma Ability Score
hp           (int): Character character's starting hitpoint value
mp           (int): Character character's starting mp value
```
In addition, the Character object can receive attributes that are normally set automatically, such as the UUID. This is for re-loading the objects from serialized data (via `Character(**characterData)`) and probably aren't arguments you would write manually into your code.


## Experience and Levels

Experience has multiple methods in this library.  However, only two of them should ever be directly called.  These two methods would be `object.giveExp(amount)` and `object.removeExp(amount)`.  The rest of the Experience and Level system is automated and updated anytime experience is awarded or removed.  If you wish to get the current experience of the player, use `object.experience` to display the integer value of it.

#### Examples
```python
# Set Character Object
newCharacter = Character(name='Bob Ross',
		   level=1)

# Current Experience
print("Current Experience:", newCharacter.experience)

# Experience until next level
print("Experience until Level Up:", newCharacter.nextLvlExperience)

# Give experience
newCharacter.giveExp(100)

# Display new, updated Experience
print("Current Experience:", newCharacter.experience)

# Display new, updated Experience until next level
print("Experience until Level Up:", newCharacter.nextLvlExperience)

# Display players current level
print("Current Level:", newCharacter.level)

# Lets level up the player
newCharacter.giveExp(1000) # required Exp to reach level 2
print("Current Level:", newCharacter.level)
print("Current Experience:", newCharacter.experience)
print("Experience until Level Up:", newCharacter.nextLvlExperience)
```
