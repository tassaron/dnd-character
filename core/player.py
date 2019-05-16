from uuid import uuid4
import math

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
			self.getExpForNextLevel
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
		self.currentExperience += xp
		if (self.LeveledUp()):
			self.levelUp()

	def LeveledUp(self):
		if self.currentExperience > self.nextLvlExperience:
			return True
		else:
			return False

	def getCurrentExperience(self):
		x = self.level*(self.level-1)*500
		self.currentExperience = x

	def getExpForNextLevel(self):
		x = self.level*(self.level)*500
		self.nextLvlExperience = x - self.experience

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

