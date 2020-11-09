from uuid import uuid4, UUID
from functools import reduce
import math
import logging

from .roll import RollStats
from .SRD import SRD
from .experience import Experience, experience_at_level


LOG = logging.getLogger(__package__)


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
        class_index: str = None,
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
        cantrips_known: dict = None,
        spells_known: dict = None,
        spells_prepared: list = None,
        spell_slots: dict = None,
        skills_strength: dict = None,
        skills_dexterity: dict = None,
        skills_wisdom: dict = None,
        skills_intelligence: dict = None,
        skills_charisma: dict = None,
        inventory: list = None,
        prof_bonus: int = 0,
        ability_score_bonus: int = 0,
        class_features: dict = None,
        class_spellcasting: dict = None,
        class_features_enabled: list = None,
        spellcasting_stat: str = None,
        player_options: dict = None,
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
        self.player_options = (
            player_options if player_options is not None else {"starting_equipment": []}
        )

        self.alignment = alignment
        if self.alignment is not None:
            assert (
                len(self.alignment) == 2
            ), "Alignments must be 2 letters (i.e LE, LG, TN, NG, CN)"
            self.alignment = self.alignment.upper()

        self.wealth = wealth
        self.class_name = class_name
        self.class_index = class_index
        self.class_levels = class_levels if class_levels is not None else []
        self.prof_bonus = prof_bonus
        self.ability_score_bonus = ability_score_bonus
        self.class_features = class_features if class_features is not None else {}
        self.class_features_enabled = (
            class_features_enabled if class_features_enabled is not None else []
        )
        self.class_spellcasting = (
            class_spellcasting if class_spellcasting is not None else {}
        )
        self._level = 1
        self._experience = Experience(character=self, experience=experience)
        if level != self._level:
            if self._experience.experience == 0:
                # if only level is specified, set the experience to the amount for that level
                self._experience.experience = experience_at_level(level)
            else:
                # the Experience object normally handles the Character object's level attr
                # but if a user changes their level manually, it should override this anyway
                LOG.info(
                    f"Custom level for {str(self.name)}: {str(level)} instead of {str(self.level)}"
                )
                self._level = level

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
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.spells_prepared = spells_prepared
        self.spell_slots = spell_slots
        self.spellcasting_stat = spellcasting_stat

        if skills_charisma is None:
            self.skills_charisma = {
                "deception": False,
                "intimidation": False,
                "performance": False,
                "persuasion": False,
            }
        else:
            self.skills_charisma = skills_charisma
        if skills_wisdom is None:
            self.skills_wisdom = {
                "animal-handling": False,
                "insight": False,
                "medicine": False,
                "perception": False,
                "survival": False,
            }
        else:
            self.skills_wisdom = skills_wisdom
        if skills_dexterity is None:
            self.skills_dexterity = {
                "acrobatics": False,
                "sleight-of-hand": False,
                "stealth": False,
            }
        else:
            self.skills_dexterity = skills_dexterity
        if skills_intelligence is None:
            self.skills_intelligence = {
                "arcana": False,
                "history": False,
                "investigation": False,
                "nature": False,
                "religion": False,
            }
        else:
            self.skills_intelligence = skills_intelligence
        if skills_strength is None:
            self.skills_strength = {
                "athletics": False,
            }
        else:
            self.skills_strength = skills_strength

        self.inventory = inventory if inventory is not None else []

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
            f"EXP to next Level: {str(self.experience.to_next_level)}\n\n"
            f"Proficiencies:\n{', '.join([value['name'] for value in self.proficiencies.values()])}\n\n"
            f"Inventory:\n{', '.join([item['name'] for item in self.inventory])}\n\n"
            f"Class Features:\n{', '.join([item['name'] for item in self.class_features.values()])}\n\n"
        )

    def keys(self):
        keys = [key for key in self.__dict__ if not key.startswith("_")]
        keys.append("experience")
        return keys

    def values(self):
        vals = [
            value if key != "uid" else str(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        ]
        vals.append(self._experience._experience)
        return vals

    def __getitem__(self, key):
        return dict(zip(self.keys(), self.values()))[key]

    @property
    def experience(self):
        return self._experience.experience

    @experience.setter
    def experience(self, new_val):
        if new_val is None:
            pass
        elif type(new_val) is Experience:
            self._experience = new_val
        else:
            self._experience.experience = new_val

    @property
    def classs(self):
        return self.__class

    @classs.setter
    def classs(self, new_class):
        self.__class = new_class
        if new_class is not None:
            self.class_name = new_class["name"]
            self.class_index = new_class["index"]
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

            starting_equipment = SRD(new_class["starting_equipment"])
            for item in starting_equipment["starting_equipment"]:
                for i in range(item["quantity"]):
                    self.giveItem(SRD(item["equipment"]["url"]))

            self.player_options["starting_equipment"] = []
            for item_option in starting_equipment["starting_equipment_options"]:
                options = []
                if hasattr(item_option["from"], "get"):
                    options.append(
                        item_option["from"][list(item_option["from"].keys())[0]]["name"]
                    )
                else:
                    for option in item_option["from"]:
                        if "equipment_category" in option:
                            options.append(option["equipment_category"]["name"])
                        elif "equipment_option" in option:
                            options.append(
                                f'{"%s " % option["equipment_option"]["choose"] if option["equipment_option"]["choose"] != 1 else ""}{option["equipment_option"]["from"]["equipment_category"]["name"]}'
                            )
                        elif "equipment" in option:
                            options.append(option["equipment"]["name"])
                self.player_options["starting_equipment"].append(
                    f"choose {item_option['choose']} from {', '.join(options)}"
                )

            self.class_levels = SRD(new_class["class_levels"])
            if "spellcasting" in new_class:
                self.spellcasting_stat = SRD(new_class["spellcasting"])[
                    "spellcasting_ability"
                ]["index"]
            else:
                self.spellcasting_stat = None

            self.applyClassLevel()

            return False

    def applyClassLevel(self):
        if self.level > 20:
            return
        for data in self.class_levels:
            if data["level"] > self.level:
                break
            self.ability_score_bonus = data.get(
                "ability_score_bonuses", self.ability_score_bonus
            )
            self.prof_bonus = data.get("prof_bonus", self.prof_bonus)
            for feat in data["features"]:
                self.class_features[feat["index"]] = SRD(feat["url"])
            while len(self.class_features_enabled) < len(self.class_features):
                self.class_features_enabled.append(True)
            self.class_spellcasting = data.get("spellcasting", self.class_spellcasting)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level
        self.applyClassLevel()

    def giveItem(self, item):
        self.inventory.append(item)

    def removeItem(self, item):
        self.inventory.remove(item)

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
