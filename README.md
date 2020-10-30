# dnd-character
A Python library to make Dungeons & Dragons characters for use in another app. Forked and significantly refactored from [PyDnD](https://github.com/Coffee-fueled-deadlines/PyDnD).


# Installation
1. Install from PyPI using `pip install dnd-character`
1. See `example.py` for example code on how to use the library.


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
