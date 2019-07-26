from uuid import uuid4
import math
from random import SystemRandom
import operator as op
from functools import reduce

class Player(object):

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
                          
		self.uid            = uuid4()
		self.name           = name
		self.age            = age
		self.gender         = gender
		self.description    = description
		self.biography      = biography
		self.wealth         = wealth

		if (self.wealth == None):
			self.wealth = 0

		# Levels
		self.level          = level
		if (self.level == None):
			self.level      = 1
			self.experience = 0
			self.getExpForNextLevel()
		else:
			self.getCurrentExperience()
			self.getExpForNextLevel()


		# Stats
		self.strength       = strength
		self.dexterity      = dexterity
		self.consitution    = constitution
		self.wisdom         = wisdom
		self.intelligence   = intelligence
		self.charisma       = charisma
		self.hp             = hp
		self.mp             = mp

		# Inventory
		self.inventory      = []
		self.invsize        = len(self.inventory)

	# Levels and Experience
	def giveExp(self, xp):
		self.experience += xp
		while (self.LeveledUp()):
			print('level up')
			self.levelUp()
			self.getExpForNextLevel()
		else:
			self.getExpForNextLevel()

	def LeveledUp(self):
		if self.experience >= self.nextLvlExperience:
			return True
		else:
			return False

	def getCurrentExperience(self):
		try:
			self.experience = self.experience
		except:
			self.experience = int(1000 * (self.level + Player.nCr(self.level,2))) - (self.level*1000)

	def getExpForNextLevel(self):
		if self.level == 1:
			self.lastLevelExperience = 0
			self.nextLvlExperience = 1000 - self.experience
		elif self.level > 1:
			self.lastLevelExperience = (1000 * (self.level + Player.nCr(self.level,2))) - (self.level*1000)
			self.nextLvlExperience = int((self.lastLevelExperience + ((1000 * ((self.level+1) + self.nCr((self.level+1),2))) - ((self.level+1)*1000))) - self.experience)

	def levelUp(self):
		self.getExpForNextLevel()
		self.level += 1

	# Inventory and Inventory management
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

