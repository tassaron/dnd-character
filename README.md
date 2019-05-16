# PyDnD
Python Dungeons and Dragons Library


## Example Invocation

	from core.player import Player
	from core.dice import Roll

```python
from core.player import Player
from core.dice import Roll

if __name__ == '__main__':
		
	newPlayer = Player('Thor Odinson', '34', 'Male', 'Looks like a pirate angel', 'Born on Asgard, God of Thunder')
		
	# newPlayer is created, lets display some stats
	
	print( "Name:" + newPlayer.name )
	print( "Age: " +newPlayer.age)
	print( "Gender:" + newPlayer.gender )
	print( "Description: " + newPlayer.description )
	print( "Biography: " + newPlayer.biography )
	
	print( "\n" )
	
	print( "Level: " + str( newPlayer.level ) ) # Level isn't specified in creation, so level is 1
	print( "Current Experience: " + str( newPlayer.experience ) ) # Level wasn't specified, so current xp is 0
	print( "EXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 500 Experience is required to get to level 2
  ```
