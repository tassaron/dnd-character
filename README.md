# PyDnD

**Description**:
Python Dungeons and Dragons Library utilizing SRD

**Status**:
Incomplete/In-Development

**Note**: If you like and/or want to use this, a star or a follow would be appreciated. 

## Example Invocation

```python
from PyDnD import Player
from PyDnD import Roll

if __name__ == '__main__':
		
	newPlayer = Player(name='Thor Odinson', 
			   age='34', 
			   gender='Male', 
			   description='Looks like a pirate angel', 
			   biography='Born on Asgard, God of Thunder')
		
	# newPlayer is created, lets display some stats
	print( "Name:",          newPlayer.name)
	print( "Age:",           newPlayer.age)
	print( "Gender:",        newPlayer.gender)
	print( "Description:",   newPlayer.description)
	print( "Biography:",     newPlayer.biography)
	
	print( "Level:",              newPlayer.level) # Level isn't specified in creation, so level is 1
	print( "Current Experience:", newPlayer.experience) # Level wasn't specified, so current xp is 0
	print( "EXP to next Level:",  newPlayer.nextLvlExperience) # 1000 Experience is required to get to level 2
	
	# Lets see what Thor looks like as a level 2
	newPlayer.giveExp(1000)
	print( "New Level: ",         newPlayer.level) # newPlayer.level is automatically increased when XP threshold increases
	print( "Current Experience:", newPlayer.experience) # Current, experience after leveling up
	print( "EXP to next Level:",  newPlayer.nextLvlExperience) # 3000 Experience is required to get to level 3
  ```
***

## Player Object

  The Player Object is the core of this library and should not be omitted (unless you're just using PyDnD for the Dice roller).  All arguments for the player object technically can be omitted (and added later) to create a blank, level 1 character.  However, we recommend at least giving the player object a `name`.  When Initializing the object, it's important to key the arguments with their corresponding argument name (listed below).
  
#### Player Object — Arguments
```
name         (str): Player character's name
age          (str): Player character's age
gender       (str): Player character's gender
alignment    (str): Player character's two letter alignment
description  (str): Physical description of Player character
biography    (str): Backstory of Player character	
level        (int): Player character's starting level
wealth       (int): Player character's starting wealth	
strength     (int): Player character's starting strength Ability Score
dexterity    (int): Player character's starting dexterity Ability Score
constitution (int): Player character's starting constitution Ability Score
wisdom       (int): Player character's starting wisdom Ability Score
intelligence (int): Player character's starting intelligence Ability Score
charisma     (int): Player character's starting charisma Ability Score
hp           (int): Player character's starting hitpoint value
mp           (int): Player character's starting mp value (may convert to SPD)
```

#### Examples
```python
from PyDnD import Player

# Initialize the player object with some useful, accurate information
myPlayer = Player(name        = 'John Cougar Mellencamp',
		  age         = '900',
		  gender      = 'Male',
		  alignment   = 'CG',
		  description = 'Looks like an old musician',
		  biography   = 'Is an old musician reknown for his one good song',
		  level       = 1,
		  wealth      = 100)	  
		  
# Did we put the wrong name?  That's okay!  We can change it
myPlayer.name = 'Meatloaf'
```
***

## Experience and Levels

  Experience has multiple methods in this library.  However, only two of them should ever be directly called.  These two methods would be `object.giveExp(amount)` and `object.removeExp(amount)`.  The rest of the Experience and Level system is automated and updated anytime experience is awarded or removed.  If you wish to get the current experience of the player, use `object.experience` to display the integer value of it.

#### Examples
```python
# Set Player Object
newPlayer = Player(name='Bob Ross',
		   level=1)

# Current Experience
print("Current Experience:", newPlayer.experience)

# Experience until next level
print("Experience until Level Up:", newPlayer.nextLvlExperience)

# Give experience
newPlayer.giveExp(100)

# Display new, updated Experience
print("Current Experience:", newPlayer.experience)

# Display new, updated Experience until next level
print("Experience until Level Up:", newPlayer.nextLvlExperience)

# Display players current level
print("Current Level:", newPlayer.level)

# Lets level up the player
newPlayer.giveExp(1000) # required Exp to reach level 2
print("Current Level:", newPlayer.level)
print("Current Experience:", newPlayer.experience)
print("Experience until Level Up:", newPlayer.nextLvlExperience)
```


