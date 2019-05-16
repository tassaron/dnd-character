from random import SystemRandom

class Roll(object):
	
	def __init__(self, min: int, max: int):
		self.min = min
		self.max = max
		self.dice()

	def dice(self):
		c = SystemRandom()
		self.value = c.randrange(self.min,self.max)


