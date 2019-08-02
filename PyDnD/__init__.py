#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}
"""

# Built-in/Generic Imports
import math
import operator as op
from functools import reduce
from random import SystemRandom
from uuid import uuid4

__author__ = 'Markis Cook'
__copyright__ = 'Copyright 2019, PyDnD'
__credits__ = ['Markis Cook (Lead Programmer, Creator)']
__license__ = '{license}'
__version__ = '0.1.0'
__maintainer__ = 'Markis Cook'
__email__ = 'cookm0803@gmail.com'
__status__ = 'Open'

#################
# PLAYER OBJECT #
#################
class Player(object):
	"""Player Object deals with all aspects of the player character
	
	Player Object deals with all aspects of the player character to include
	name, age, gender, description, biography, level, wealth, and all
	player Ability scores.  All can be omitted to create a blank, level 1 
	player and all values can be manually adjusted via the calling 
	application.
	
	All given Args populate self.argname
	
	Args:
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
		
	Returns:
		This object returns nothing.  Instead all Args populate self.argname
	"""

	def __init__(
		self,
		name:               str = None,
		age:                str = None, 
		gender:             str = None, 
		alignment:          str = None,
		description:        str = None,
		biography:          str = None,
		level:              int = None,
		wealth:             int = None,
		strength:           int = None,
		dexterity:          int = None,
		constitution:       int = None,
		wisdom:             int = None,
		intelligence:       int = None,
		charisma:           int = None,
		hp:                 int = None,
		mp:                 int = None):                
		"""Object Initialization
		
		Object initialization, grabs all given Args and sets them to self.argname
		note that all Args can be omitted and a Level 1, blank character will be
		generated instead.
		
		Returns:
			Nothing
		"""
                          
		self.uid            = uuid4()      # Unique identifier for given player
		self.name           = name
		self.age            = age
		self.gender         = gender
		self.description    = description
		self.biography      = biography

		# Handle Alignment
		self.alignment      = alignment
		if self.alignment != None:
			assert (len(self.alignment) == 2), "Alignments must be 2 letters (i.e LE, LG, TN, NG, CN)"
			self.alignment = self.alignment.upper()

		self.wealth         = wealth

		# If wealth is omitted, set starting wealth to 0
		if (self.wealth == None):
			self.wealth = 0

		# Levels
		self.level          = level
		
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

		self.skillpoints = 0
		self.featpoints = 0


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
		self.inventory      = []
		self.invsize        = len(self.inventory)
	
	################################
	# START: Levels and Experience #
	##############################################################################
	#                                                                            #
	# All Methods under this section deal with Incrementing/Decrementing levels  #
	# and managing experience.                                                   #
	#                                                                            #
	##############################################################################
	def giveExp(self, xp):
		"""Increment experience of player object
		
		This method increments the current self.experience of the
		player object by the amount provided.
		
		Args:
			xp (int): The amount of experience to increment self.experience by
			
		Returns:
			This method returns nothing and instead modifies self.experience
			
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
		"""Decrements experience of player object
		
		This method decrements the current self.experience of the
		player object by the amount specified
		
		Args:
			xp (int): The amount of experience to decrement self.experience by
			
		Returns:
			This method returns nothing and instead modifies self.experience
			
		Triggers:
			self.LeveledDown(): Triggered every time, checks to see if player
					    lost the experience required to maintain their
					    current level.
					    
			self.levelDown(): Triggers only if self.LeveledDown() is True
					  decrements the level of the player object
					  
			self.getExpForNextLevel(): Triggers ever time, checks the experience
			                           needed to reach the next level for the player
						   object
		"""
		self.experience -= xp
		while (self.LeveledDown()):
			self.levelDown()
		else:
			self.getExpForNextLevel()

	def LeveledUp(self):
		"""Checks to see if player has leveled up
		
		This method checks the current experience against the experience
		needed to gain the next level.  If the experience currently held is
		greater than or equal to the needed experience (nextLvlExperience)
		this method returns True, else it returns False
		
		Args:
			None
			
		Returns:
			Boolval
		"""
		if self.experience >= self.nextLvlExperience:
			return True
		else:
			return False
		
	def LeveledDown(self):
		"""Checks to see if player has leveled down
		
		This method checks the current experience against the experience
		needed to gain their previous level.  If their experience drops
		below that level, the player loses a level.
		
		Args:
			None
		
		Returns:
			Boolval
		"""
		if self.experience < self.lastLevelExperience:
			return True
		else:
			return False
		
	def getCurrentExperience(self):
		"""Calculates the current experience of player
		
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
			self.experience = int(1000 * (self.level + Player.nCr(self.level,2))) - (self.level*1000)

	def getExpForNextLevel(self):
		"""Calculates the experience needed for next level
		
		This method calculates and sets the experience that the player
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
			self.lastLevelExperience = (1000 * (self.level + Player.nCr(self.level,2))) - (self.level*1000)
			self.nextLvlExperience = int((self.lastLevelExperience + ((1000 * ((self.level+1) + self.nCr((self.level+1),2))) - ((self.level+1)*1000))) - self.experience)

	def levelUp(self):
		"""Handles player level up
		
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
		"""Handles player level down
		
		This method decrements the players level by one first and 
		then triggers the getExpForNextLevel() method.
		
		Args:
			None
			
		Returns:
			None
		"""
		# Only Decrement level if level is higher than 1
		if self.level > 1:
			self.level -= 1
		# If level is already at level 1, player cannot lose
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
	
	#############################
	# Wealth, Income, and Trade #
	#############################
	# Give wealth to player object
	def giveWealth(self, amount):
		"""Handles awarding players wealth
		
		The giveWealth() method increments the wealth of the player
		object
		
		Args:
			amount
		
		Returns:
			None
		"""
		self.wealth += amount
	
	# Remove wealth from player object
	def removeWealth(self, amount):
		"""Handles removing wealth from the player
		
		The removeWealth() method decrements the wealth of the player
		object by the amount supplied.  If the wealth of the player
		object is not sufficient, the self.wealth of the player is
		instead set to 0.
		
		Args:
			amount
			
		Returns:
			None
		"""
		if amount > self.wealth:
			self.wealth = 0
		else:
			self.wealth -= amount
			
	# Charge wealth from player object
	def chargeWealth(self, amount):
		"""Handles charging wealth from the player
		
		The chargeWealth() method functions similarly to the
		removeWealth() method.  However, instead of setting
		self.wealth to 0 on the condition of not having enough,
		chargeWealth() returns False and doesn't change the
		value of self.wealth.  On success, self.removeWealth()
		is triggered, the amount is removed, and chargeWealth()
		returns True.
		
		Args:
			amount
			
		Returns:
			Boolval
			
		Triggers:
			self.removeWealth(): Triggers if self.wealth of
			                     player object contains enough
					     wealth to remove amount from.
		"""
		if amount > self.wealth:
			# Not enough for purchase
			return False
		else:
			self.removeWealth(self, amount)
			return True

	# Class Methods
	@classmethod
	def nCr(self,n,r):
		r = min(r, n-r)
		numer = reduce(op.mul, range(n, n-r, -1),1)
		denom = reduce(op.mul, range(1, r+1), 1)
		return numer / denom
	
	@classmethod
	def setInitialAbilityScore(self, stat):
		"""Handles setting initial Ability Scores
		
		The setInitialAbilityScore() method accepts a Stat arg.  If Stat is
		None, then this method instead Rolls for the initial starting ability
		score using the standard rolling method.
		
		Args:
			stat
			
		Returns:
			roll: the RollStats() object.  Get value with roll.value
			int(stat): The integer value of the supplied stat
		"""
		if stat == None:
			roll = RollStats()
			return roll
		else:
			return int(stat)
	
	@classmethod
	def getModifier(self,stat):
		"""Returns modifier for given stat

		This method returns the modifier for the given stat provided

		Args:
			stat (int): The player ability score to calculate the modifier for

		Returns:
			modifier  (int): The modifier for the given stat
			None (NoneType): Returns none if the ability score queried doesn't exist
		"""
		modifier = math.floor(stat/2)-5
		return modifier	

###############
# Roll Object #
###############
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


#############
# STAT ROLL #		
#############
class RollStats(object):
	
	def __init__(self, method: str=None):
		self.method = method

	def stat_roller(self):
		if self.method.lower() in [None, 'standard', '4d6d1', '4d6dl']:
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

		elif self.method.lower() == "3d6" or "classic":
			# Roll 4D6 drop lowerest method
			statNumber = 0
			self.rollList = []
			for i in range(3):
				dice = Roll(1,6)
				statNumber += dice.value
				self.rollList.append(dice.value)
			self.statroll = int(statNumber)

		elif self.method.lower() == "heroic" or "2d6+6":
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
		
		
		
