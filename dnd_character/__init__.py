#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
dnd-character is a Python package for integrating DnD characters
into external applications.
"""

# Built-in/Generic Imports
import math
import operator as op
from functools import reduce
from random import SystemRandom
from uuid import uuid4, UUID

__author__ = 'Brianna Rainey'
__copyright__ = 'Copyright 2020'
__credits__ = ['Brianna Rainey (Current Programmer)', 'Markis Cook (Original Creator)']
__license__ = 'EPL-2.0'
__version__ = '0.1.0'
__maintainer__ = 'Brianna Rainey'


class Character:
	"""
	Character Object deals with all aspects of the player character including
	name, age, gender, description, biography, level, wealth, and all
	player ability scores.  All can be omitted to create a blank, level 1 
	player.
	"""

	def __init__(
		self,
		uid:               UUID = None,
		name:               str = None,
		age:                str = None, 
		gender:             str = None, 
		alignment:          str = None,
		description:        str = None,
		biography:          str = None,
		level:              int = None,
		experience:         int = 0,
		wealth:             int = None,
		strength:           int = None,
		dexterity:          int = None,
		constitution:       int = None,
		wisdom:             int = None,
		intelligence:       int = None,
		charisma:           int = None,
		hp:                 int = None,
		mp:                 int = None,
		skillpoints:        int = 0,
		featpoints:         int = 0,
		lastLevelExperience:int = None,
		nextLvlExperience:  int = None,
		inventory:          list= None,
		invsize:            int = None):                
		"""
		Typical Arguments:
			name         (str)
			age          (str)
			gender       (str)
			alignment    (str): two letter alignment (LE, TN, CN, LG, etc.)
			description  (str): physical description of character
			biography    (str): backstory of character
			level        (int): character's starting level
			wealth       (int): character's starting wealth
			strength     (int): character's starting strength
			dexterity    (int):  character's starting dexterity
			constitution (int):  character's starting constitution
			wisdom       (int):  character's starting wisdom
			intelligence (int):  character's starting intelligence
			charisma     (int):  character's starting charisma
			hp           (int):  character's starting hitpoint value
			mp           (int):  character's starting mp value
		"""
                          
		self.uid            = UUID(uid) if uid is not None else uuid4()   # Unique identifier for given player
		self.name           = name
		self.age            = age
		self.gender         = gender
		self.description    = description
		self.biography      = biography

		self.alignment      = alignment
		if self.alignment != None:
			assert (len(self.alignment) == 2), "Alignments must be 2 letters (i.e LE, LG, TN, NG, CN)"
			self.alignment = self.alignment.upper()

		self.wealth         = wealth
		if (self.wealth == None):
			self.wealth = 0

		self.level          = level
		self.experience     = experience
		
		# If level is omitted, set starting level to 1
		if (self.level == None):
			self.level      = 1
			self.experience = 0
			self.getExpForNextLevel()
		# If level not omitted, calculate the starting experience for
		# provided level
		else:
			self.getCurrentExperience()
			self.getExpForNextLevel()

		# Sanity check
		if lastLevelExperience is not None:
			assert self.lastLevelExperience == lastLevelExperience 
		if nextLvlExperience is not None:
			assert self.nextLvlExperience == nextLvlExperience

		self.skillpoints = skillpoints
		self.featpoints = featpoints


		# Ability Scores
		self.strength       = self.setInitialAbilityScore(strength)
		self.dexterity      = self.setInitialAbilityScore(dexterity)
		self.constitution   = self.setInitialAbilityScore(constitution)
		self.wisdom         = self.setInitialAbilityScore(wisdom)
		self.intelligence   = self.setInitialAbilityScore(intelligence)
		self.charisma       = self.setInitialAbilityScore(charisma)

		self.hp             = hp
		self.mp             = mp

		# Inventory (currently primitive)
		self.inventory      = inventory if inventory is not None else []
		self.invsize        = len(self.inventory)

	def __str__(self):
		return (
			f"Name: {self.name}\n"
			f"Age: {self.age}\n"
			f"Gender: {self.gender}\n"
			f"Description: {self.description}\n"
			f"Biography:\n{self.biography}\n\n"
			f"Level: {str(self.level)}\n"
			f"Current Experience: {str(self.experience)}\n"
			f"EXP to next Level: {str(self.nextLvlExperience)}\n"
		)

	def keys(self):
		return [key for key in self.__dict__ if not key.startswith("__")]

	def values(self):
		return [
			value if key != "uid" else str(value)
			for key, value in self.__dict__.items() if not key.startswith("__")
		]

	def __getitem__(self, key):
		return dict(zip(self.keys(), self.values()))[key]

	def giveExp(self, xp):
		"""
		Increments the current self.experience of the
		character object by the amount provided.
			
		Triggers:
			self.LeveledUp(): Triggers every time, checks to see if player
					  has gained the experience required to acheive
					  the next level.
					  
			self.levelUp(): Triggers when self.LeveledUp() is True, increments
					the player object's level by one and gets the
					experience needed for the next level.
					
			self.getExpForNextLevel(): Triggers when self.LeveledUp() is False
						   and gets the Experience needed for the 
						   next level.
		"""
		self.experience += xp
		while (self.LeveledUp()):
			self.levelUp()
		else:
			self.getExpForNextLevel()
			
	def removeExp(self, xp):
		"""
		Decrements the current self.experience of the
		character object by the amount specified

		Triggers:
			self.LeveledDown(): Triggered every time, checks to see if player
					    lost the experience required to maintain their
					    current level.
					    
			self.levelDown(): Triggers only if self.LeveledDown() is True
					  decrements the level of the character object
					  
			self.getExpForNextLevel(): Triggers ever time, checks the experience
			                           needed to reach the next level for the character
						   object
		"""
		self.experience -= xp
		while (self.LeveledDown()):
			self.levelDown()
		else:
			self.getExpForNextLevel()

	def LeveledUp(self):
		"""
		Checks to see if character has leveled up
		
		This method checks the current experience against the experience
		needed to gain the next level. If the experience currently held is
		greater than or equal to the needed experience (nextLvlExperience)
		this method returns True, else it returns False
		"""
		if self.experience >= self.nextLvlExperience:
			return True
		else:
			return False
		
	def LeveledDown(self):
		"""
		Checks to see if character has leveled down
		
		This method checks the current experience against the experience
		needed to gain their previous level. If their experience drops
		below that level, the character loses a level.
		"""
		if self.experience < self.lastLevelExperience:
			return True
		else:
			return False
		
	def getCurrentExperience(self):
		"""
		Calculates the current experience
		
		This method calculates and sets the current experience of the
		player character.  If self.experience has not been set (in
		the event of a new character) then this method instead sets
		the current self.experience to the experience amount for that
		given level.
		
		Args:
			None
			
		Returns:
			None
		"""
		try:
			self.experience = self.experience
		except:
			self.experience = int(1000 * (self.level + Character.nCr(self.level,2))) - (self.level*1000)

	def getExpForNextLevel(self):
		"""Calculates the experience needed for next level
		
		This method calculates and sets the experience that the character
		requires to reach the next level given their current experience.
		
		Args:
			None
			
		Returns:
			None
		"""
		if self.level == 1:
			self.lastLevelExperience = 0
			self.nextLvlExperience = 1000 - self.experience
		elif self.level > 1:
			self.lastLevelExperience = (1000 * (self.level + Character.nCr(self.level,2))) - (self.level*1000)
			self.nextLvlExperience = int((self.lastLevelExperience + ((1000 * ((self.level+1) + self.nCr((self.level+1),2))) - ((self.level+1)*1000))) - self.experience)

	def levelUp(self):
		"""Handles character level up
		
		This method triggers the getExpForNextLevel() method and then
		increments the player character's level by one.
		
		Args:
			None
			
		Returns:
			None
		"""
		self.getExpForNextLevel()
		self.level += 1
		
	def levelDown(self):
		"""Handles character level down
		
		This method decrements the characters level by one first and 
		then triggers the getExpForNextLevel() method.
		
		Args:
			None
			
		Returns:
			None
		"""
		# Only Decrement level if level is higher than 1
		if self.level > 1:
			self.level -= 1
		# If level is already at level 1, character cannot lose
		# a level and instead is reduced to 0 experience.
		else:
			self.level = 1
			self.experience = 0
		# Regardless, get Experience for next Level
		self.getExpForNextLevel()
		##############################
		# END: Levels and Experience #
		##############################
		
	# Inventory and Inventory management (Primitive)
	def getInventorySize(self):
		self.invsize = len(self.inventory)
		return self.invsize

	def updateInventory(self):
		self.invsize = len(self.inventory)

	def giveItem(self, item):
		self.inventory.append(item)
		self.updateInventory()

	def removeItem(self, item):
		self.inventory.remove(item)
		self.updateInventory()
	
	def giveWealth(self, amount):
		"""
		Give wealth to character

		Args:
			amount
			
		Returns:
			None
		"""
		self.wealth += amount
	
	def removeWealth(self, amount):
		"""
		Remove wealth from character

		Args:
			amount

		Returns:
			None
		"""
		if amount > self.wealth:
			self.wealth = 0
		else:
			self.wealth -= amount
			
	def chargeWealth(self, amount):
		"""
		The chargeWealth() method functions similarly to the
		removeWealth() method. However, instead of setting
		self.wealth to 0 on the condition of not having enough,
		chargeWealth() returns False and doesn't change the
		value of self.wealth. On success, self.removeWealth()
		is triggered, the amount is removed, and chargeWealth()
		returns True.
		
		Args:
			amount
			
		Returns:
			Boolval
			
		Triggers:
			self.removeWealth() if self.wealth > amount
		"""
		if amount > self.wealth:
			# Not enough for purchase
			return False
		else:
			self.removeWealth(self, amount)
			return True

	@classmethod
	def nCr(self,n,r):
		r = min(r, n-r)
		numer = reduce(op.mul, range(n, n-r, -1),1)
		denom = reduce(op.mul, range(1, r+1), 1)
		return numer / denom
	
	@classmethod
	def setInitialAbilityScore(self, stat):
		"""
		Set ability score to an int. If the argument is None, then this method
		instead rolls for the initial starting ability score.
		
		Args:
			stat
			
		Returns:
			the new ability score as an int
		"""
		if stat == None:
			roll = RollStats()
			return roll.stat_roller()
		else:
			return int(stat)
	
	@classmethod
	def getModifier(self, stat):
		"""
		This method returns the modifier for the given stat

		Args:
			stat (int): The player ability score to calculate the modifier for

		Returns:
			modifier  (int): The modifier for the given stat
			None (NoneType): Returns none if the ability score queried doesn't exist
		"""
		modifier = math.floor(stat/2)-5
		return modifier	


######################
# START: ROLL OBJECT #
######################
class Roll(object):
	"""Creates roll values

	The Roll object creates roll values for dice rolls.  Random values are created from
	SystemRandom (using system entropy) to create a better pseudorandom number.

	Args:
		min (int): the minimum number to roll
		max (int): the maximum number to roll

	Returns:
		This object returns nothing and instead sets the value of self.value
		to be called at a later time.
	"""
	def __init__(self, min: int, max: int, modifier: int = 0):
		self.min = min
		self.max = max+1
		self.modifier = modifier
		self.dice()

	def dice(self):
		c = SystemRandom()
		self.value = c.randrange(self.min,self.max)	+ self.modifier
	######################
	#  END: ROLL OBJECT  #
	######################
###########################
# START: ROLLSTATS OBJECT #		
###########################
class RollStats(object):
	
	def __init__(self, method: str=None):
		self.method = method if method is None else method.lower()

	def stat_roller(self):
		if self.method in [None, 'standard', '4d6d1', '4d6dl']:
			#default method
			statNumber = 0
			self.rollList = []
			for i in range(4):
				dice = Roll(1,6)
				statNumber += dice.value
				self.rollList.append(dice.value)
			statNumber -= min(self.rollList)
			self.rollList.remove(min(self.rollList))
			self.statroll = int(statNumber)

		elif self.method == "3d6" or "classic":
			# Roll 4D6 drop lowerest method
			statNumber = 0
			self.rollList = []
			for i in range(3):
				dice = Roll(1,6)
				statNumber += dice.value
				self.rollList.append(dice.value)
			self.statroll = int(statNumber)

		elif self.method == "heroic" or "2d6+6":
			# Roll 2d6 and add 6 to that number
			statNumber = 0
			self.rollList = []
			for i in range(2):
				dice = Roll(1,6)
				statNumber += dice.value
				self.rollList.append(dice.value)
			self.statroll = int(statNumber + 6)

		else:
			raise "Accepted values are, 'standard','classic', and 'heroic' roll methods."

		return self.statroll

	###########################
	#  END: ROLLSTATS OBJECT  #
	###########################
#######
# EOF #
#######
