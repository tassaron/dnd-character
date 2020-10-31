from uuid import uuid4, UUID
from functools import reduce
import math
import operator as op

from .roll import RollStats
from .SRD import SRD


class Character:
    """
    Character Object deals with all aspects of the player character including
    name, age, gender, description, biography, level, wealth, and all
    player ability scores.  All can be omitted to create a blank, level 1
    player.
    """

    def __init__(
        self,
        uid: UUID = None,
        name: str = None,
        age: str = None,
        gender: str = None,
        alignment: str = None,
        description: str = None,
        biography: str = None,
        classs: dict = None,
        class_name: str = None,
        class_levels: list = None,
        level: int = 1,
        experience: int = 0,
        wealth: int = 0,
        strength: int = None,
        dexterity: int = None,
        constitution: int = None,
        wisdom: int = None,
        intelligence: int = None,
        charisma: int = None,
        hp: int = None,
        hd: str = None,
        proficiencies: dict = None,
        saving_throws: list = None,
        spells: dict = None,
        spells_prepared: list = None,
        spell_slots: dict = None,
        skills_strength: dict = None,
        skills_dexterity: dict = None,
        skills_wisdom: dict = None,
        skills_intelligence: dict = None,
        skills_charisma: dict = None,
        lastLevelExperience: int = None,
        nextLvlExperience: int = None,
        inventory: list = None,
        invsize: int = None,
        prof_bonus: int = 0,
        ability_score_bonus: int = 0,
        class_features: dict = None,
    ):
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
        """

        self.uid = UUID(uid) if uid is not None else uuid4()
        self.name = name
        self.age = age
        self.gender = gender
        self.description = description
        self.biography = biography

        self.alignment = alignment
        if self.alignment is not None:
            assert (
                len(self.alignment) == 2
            ), "Alignments must be 2 letters (i.e LE, LG, TN, NG, CN)"
            self.alignment = self.alignment.upper()

        self.wealth = wealth
        self.class_name = class_name
        self.class_levels = class_levels if class_levels is not None else []
        self.experience = experience

        if level is None:
            self.level = 0
            self.levelUp()
        else:
            self.level = level
        self.getCurrentExperience()
        self.getExpForNextLevel()

        # Sanity check
        if lastLevelExperience is not None:
            assert self.lastLevelExperience == lastLevelExperience
        if nextLvlExperience is not None:
            assert self.nextLvlExperience == nextLvlExperience

        # Ability Scores
        self.strength = self.setInitialAbilityScore(strength)
        self.dexterity = self.setInitialAbilityScore(dexterity)
        self.constitution = self.setInitialAbilityScore(constitution)
        self.wisdom = self.setInitialAbilityScore(wisdom)
        self.intelligence = self.setInitialAbilityScore(intelligence)
        self.charisma = self.setInitialAbilityScore(charisma)

        # Spells, Skills, Proficiencies
        self.hp = hp
        self.hd = hd
        self.proficiencies = proficiencies if proficiencies is not None else {}
        self.saving_throws = saving_throws if saving_throws is not None else []
        self.spells = spells
        self.spells_prepared = spells_prepared
        self.spell_slots = spell_slots
        self.skills_charisma = skills_charisma
        self.skills_wisdom = skills_wisdom
        self.skills_dexterity = skills_dexterity
        self.skills_intelligence = skills_intelligence
        self.skills_strength = skills_strength

        # Inventory (currently primitive)
        self.inventory = inventory if inventory is not None else []
        self.invsize = len(self.inventory)

        self.prof_bonus = prof_bonus
        self.ability_score_bonus = ability_score_bonus
        self.class_features = class_features if class_features is not None else {}
        self.classs = classs

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Description: {self.description}\n"
            f"Biography:\n{self.biography}\n\n"
            f"Class: {self.class_name}\n"
            f"Level: {str(self.level)}\n"
            f"Current Experience: {str(self.experience)}\n"
            f"EXP to next Level: {str(self.nextLvlExperience)}\n\n"
            f"Proficiencies:\n{', '.join([value['name'] for value in self.proficiencies.values()])}\n\n"
            f"Inventory:\n{', '.join([item['name'] for item in self.inventory])}\n\n"
            f"Class Features:\n{', '.join([item['name'] for item in self.class_features.values()])}\n\n"
        )

    def keys(self):
        return [key for key in self.__dict__ if not key.startswith("_")]

    def values(self):
        return [
            value if key != "uid" else str(value)
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        ]

    def __getitem__(self, key):
        return dict(zip(self.keys(), self.values()))[key]

    @property
    def classs(self):
        return self.__class

    @classs.setter
    def classs(self, new_class):
        self.__class = new_class
        if new_class is not None:
            self.class_name = new_class["name"]
            self.hd = new_class["hit_die"]

            # create dict such as { "all-armor": {"name": "All armor", "type": "Armor"} }
            for proficiency in new_class["proficiencies"]:
                data = SRD(proficiency["url"])
                self.proficiencies[proficiency["index"]] = {
                    "name": data["name"],
                    "type": data["type"],
                }

            self.saving_throws = [
                saving_throw["name"] for saving_throw in new_class["saving_throws"]
            ]

            for item in SRD(new_class["starting_equipment"])["starting_equipment"]:
                for i in range(item["quantity"]):
                    self.giveItem(SRD(item["equipment"]["url"]))

            self.class_levels = SRD(new_class["class_levels"])
            self.applyClassLevel()

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
        while self.LeveledUp():
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
        while self.LeveledDown():
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
            self.experience = int(
                1000 * (self.level + Character.nCr(self.level, 2))
            ) - (self.level * 1000)

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
            self.lastLevelExperience = (
                1000 * (self.level + Character.nCr(self.level, 2))
            ) - (self.level * 1000)
            self.nextLvlExperience = int(
                (
                    self.lastLevelExperience
                    + (
                        (1000 * ((self.level + 1) + self.nCr((self.level + 1), 2)))
                        - ((self.level + 1) * 1000)
                    )
                )
                - self.experience
            )

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
        self.applyClassLevel()

    def applyClassLevel(self):
        if self.level <= len(self.class_levels):
            data = self.class_levels[self.level - 1]
            self.ability_score_bonus = data.get(
                "ability_score_bonuses", self.ability_score_bonus
            )
            self.prof_bonus = data.get("prof_bonus", self.prof_bonus)
            for feat in data["features"]:
                self.class_features[feat["index"]] = SRD(feat["url"])

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
    def nCr(self, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
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
        modifier = math.floor(stat / 2) - 5
        return modifier
