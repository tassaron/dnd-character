# PyDnD
Python Dungeons and Dragons Library


## Example Invocation

```python
from core.player import Player
from core.player import Roll

if __name__ == '__main__':
		
	newPlayer = Player(name='Thor Odinson', age='34', gender='Male', description='Looks like a pirate angel', biography='Born on Asgard, God of Thunder')
		
	# newPlayer is created, lets display some stats
	Dice = Roll(1,20)
	print(Dice.value)
	
	print( "Name:" + newPlayer.name )
	print( "Age: " +newPlayer.age)
	print( "Gender:" + newPlayer.gender )
	print( "Description: " + newPlayer.description )
	print( "Biography: " + newPlayer.biography )
	
	print( "\n" )
	
	print( "Level: " + str( newPlayer.level ) ) # Level isn't specified in creation, so level is 1
	print( "Current Experience: " + str( newPlayer.experience ) ) # Level wasn't specified, so current xp is 0
	print( "EXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 500 Experience is required to get to level 2
	print("\n\n\n")
	# Lets see what Thor looks like as a level 2

	newPlayer.giveExp(1000)
	print( "New Level: " + str( newPlayer.level ) )
	print( "Current Experience: " + str( newPlayer.experience ) ) # Level wasn't specified, so current xp is 0
	print( "EXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 500 Experience is required to get to level 2
  ```
