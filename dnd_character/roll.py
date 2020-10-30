from random import SystemRandom


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
        self.max = max + 1
        self.modifier = modifier
        self.dice()

    def dice(self):
        c = SystemRandom()
        self.value = c.randrange(self.min, self.max) + self.modifier


class RollStats(object):
    def __init__(self, method: str = None):
        self.method = method if method is None else method.lower()

    def stat_roller(self):
        if self.method in [None, "standard", "4d6d1", "4d6dl"]:
            # default method
            statNumber = 0
            self.rollList = []
            for i in range(4):
                dice = Roll(1, 6)
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
                dice = Roll(1, 6)
                statNumber += dice.value
                self.rollList.append(dice.value)
            self.statroll = int(statNumber)

        elif self.method == "heroic" or "2d6+6":
            # Roll 2d6 and add 6 to that number
            statNumber = 0
            self.rollList = []
            for i in range(2):
                dice = Roll(1, 6)
                statNumber += dice.value
                self.rollList.append(dice.value)
            self.statroll = int(statNumber + 6)

        else:
            raise "Accepted values are, 'standard','classic', and 'heroic' roll methods."

        return self.statroll
