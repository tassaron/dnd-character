from uuid import uuid4
import math
from random import SystemRandom
import operator as op
from functools import reduce

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


		# Ability Scores
		self.strength       = strength
		self.dexterity      = dexterity
		self.consitution    = constitution
		self.wisdom         = wisdom
		self.intelligence   = intelligence
		self.charisma       = charisma
		self.hp             = hp
		self.mp             = mp

		# Inventory (currently primitive)
		self.inventory      = []
		self.invsize        = len(self.inventory)

	# Levels and Experience
	def giveExp(self, xp):
		"""Increment experience of player object
		
		This method increments the current self.experience of the
		player object by the amount provided.
		
		Args:
			xp (int): The amount of experience to increment self.experience by
			
		Returns:
			This method returns nothing and instead modifies self.experience
		"""
		self.experience += xp
		while (self.LeveledUp()):
			self.levelUp()
			self.getExpForNextLevel()
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

	# Wealth, Income, and Trade
	def giveWealth(self, amount):
		self.wealth = self.wealth + amount

	# Utility Methods
	@staticmethod
	def getModifier(a):
		modifier = math.floor(a/2)-5
		return modifier

	# Class Methods
	@classmethod
	def nCr(self,n,r):
		r = min(r, n-r)
		numer = reduce(op.mul, range(n, n-r, -1),1)
		denom = reduce(op.mul, range(1, r+1), 1)
		return numer / denom

class Roll(object):
	
	def __init__(self, min: int, max: int):
		self.min = min
		self.max = max
		self.dice()

	def dice(self):
		c = SystemRandom()
		self.value = c.randrange(self.min,self.max)		

