from typing import Optional, Union
from uuid import uuid4, UUID
import math
import logging

from .SRD import SRD, SRD_class_levels
from .experience import Experience, experience_at_level, level_at_experience
from .dice import sum_rolls


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
        *,  # This * forces the caller to use keyword arguments
        uid: UUID = None,
        name: str = None,
        age: str = None,
        gender: str = None,
        species: str = None,
        speed: int = None,
        alignment: str = None,
        description: str = None,
        background: str = None,
        personality: str = None,
        ideals: str = None,
        bonds: str = None,
        flaws: str = None,
        classs: dict = None,
        class_name: str = None,
        class_index: str = None,
        class_levels: list = None,
        level: Union[int, None] = None,
        experience: Union[int, None, Experience] = None,
        wealth: int = 0,
        strength: int = None,
        dexterity: int = None,
        constitution: int = None,
        wisdom: int = None,
        intelligence: int = None,
        charisma: int = None,
        max_hp: int = None,
        current_hp: int = None,
        temp_hp: int = None,
        hd: int = 8,
        max_hd: int = None,
        current_hd: int = None,
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
        armor_class: int = None,
        death_saves: int = 0,
        death_fails: int = 0,
        exhaustion: int = 0,
        dead: bool = False,
        conditions: dict = None,
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
        """

        # Decorative attrs that don't affect program logic
        self.uid = UUID(uid) if uid is not None else uuid4()
        self.name = name
        self.age = age
        self.gender = gender
        self.description = description
        self.background = background
        self.personality = personality
        self.ideals = ideals
        self.bonds = bonds
        self.flaws = flaws
        self.species = species
        self.speed = 30 if speed is None else int(speed)
        self.player_options = (
            player_options if player_options is not None else {"starting_equipment": []}
        )
        self.alignment = alignment
        if self.alignment is not None:
            assert (
                len(self.alignment) == 2
            ), "Alignments must be 2 letters (i.e LE, LG, TN, NG, CN)"
            self.alignment = self.alignment.upper()

        # DND Class
        self.class_name = class_name
        self.class_index = class_index
        self._class_levels = (
            [] if class_index not in SRD_class_levels else SRD_class_levels[class_index]
        )
        self.prof_bonus = prof_bonus
        self.ability_score_bonus = ability_score_bonus
        self.class_features = class_features if class_features is not None else {}
        self.class_features_enabled = (
            class_features_enabled if class_features_enabled is not None else []
        )
        self.class_spellcasting = (
            class_spellcasting if class_spellcasting is not None else {}
        )

        # Ability Scores
        self.strength = self.setInitialAbilityScore(strength)
        self._dexterity = self.setInitialAbilityScore(dexterity)
        self.constitution = self.setInitialAbilityScore(constitution)
        self.wisdom = self.setInitialAbilityScore(wisdom)
        self.intelligence = self.setInitialAbilityScore(intelligence)
        self.charisma = self.setInitialAbilityScore(charisma)

        # Hit Dice and Hit Points: self.hd == 8 is a d8, 10 is a d10, etc
        self.hd = 8 if hd is None else hd
        self.max_hd = 1 if max_hd is None else max_hd
        self.current_hd = 1 if current_hd is None else current_hd
        self.max_hp = (
            Character.maximum_hp(
                self.hd, 1 if level is None else int(level), self.constitution
            )
            if max_hp is None
            else max_hp
        )
        self._current_hp = current_hp if current_hp is not None else int(self.max_hp)
        self.temp_hp = 0 if temp_hp is None else int(temp_hp)

        # Experience points
        self._level = 1
        # self.level could be altered by Experience object below
        if experience is None:
            experience = 0
        self._experience = Experience(character=self, experience=int(experience))

        # Levels
        # self.level could be altered by Experience object above
        if level is not None:
            if self._experience.experience == 0:
                # if only level is specified, set the experience to the amount for that level
                self._experience.experience = experience_at_level(level)
                # Experience alters self.level so it is now the correct value
            else:
                # if level is specified AND experience is not zero:
                # the Experience object normally handles the self.level attr
                # but if a user changes their level manually, it should override this anyway
                LOG.info(
                    f"Custom level for {str(self.name)}: {str(level)} instead of {str(self.level)}"
                )
                self._level = level

        # Spells, Skills, Proficiencies
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

        # Inventory & Wealth
        self.wealth = wealth
        self.inventory = []
        if inventory is not None:
            for item in inventory:
                self.giveItem(item)

        # Final steps of initialization -- the classs.setter does lots of work here
        # setting the self.classs attr applies "class features" appropriate to character's level
        self.classs = classs

        # base armor class is 10 + DEX; will be affected by inventory
        if armor_class is not None:
            self.armor_class = armor_class
        elif not hasattr(self, "armor_class"):
            self.armor_class = self.baseArmorClass
        self._dead = dead
        self._death_saves = death_saves
        self._death_fails = death_fails
        self.exhaustion = int(exhaustion)

        if self.level == level_at_experience(self._experience._experience):
            self.level = self._level
            if current_hp is None:
                # Set character's HP to the maximum for their level,
                # only if the level isn't custom! (if it matches experience points according to SRD)
                self.current_hp = Character.maximum_hp(
                    self.hd, self.level, self.constitution
                )

        # Conditions
        all_conditions = [
            "blinded",
            "charmed",
            "deafened",
            "frightened",
            "grappled",
            "incapacitated",
            "invisible",
            "paralyzed",
            "petrified",
            "poisoned",
            "prone",
            "restrained",
            "stunned",
            "unconscious",
        ]
        if conditions is None:
            conditions = {}
        for condition in all_conditions:
            if condition not in conditions:
                conditions[condition] = False

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Background:\n{self.background}\n\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Description: {self.description}\n"
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
        keys.extend(
            [
                "experience",
                "death_saves",
                "death_fails",
                "dexterity",
                "dead",
                "current_hp",
            ]
        )
        return keys

    def values(self):
        vals = [
            value if key != "uid" else str(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        ]
        vals.extend(
            [
                self._experience._experience,
                self._death_saves,
                self._death_fails,
                self._dexterity,
                self._dead,
                self._current_hp,
            ]
        )
        return vals

    def __getitem__(self, key):
        return dict(zip(self.keys(), self.values()))[key]

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, new_value: bool):
        self._dead = new_value
        self._death_saves = 0
        self._death_fails = 0

    @property
    def death_saves(self):
        return self._death_saves

    @death_saves.setter
    def death_saves(self, new_value: int):
        if not 4 > new_value > -1:
            raise ValueError("Death saving throws must be in range 0-3")
        elif new_value == 3:
            self._death_saves = 0
            self._death_fails = 0
            self._dead = False
        else:
            self._death_saves = new_value

    @property
    def death_fails(self):
        return self._death_fails

    @death_fails.setter
    def death_fails(self, new_value: int):
        if not 4 > new_value > -1:
            raise ValueError("Death saving throws must be in range 0-3")
        elif new_value == 3:
            self._death_saves = 0
            self._death_fails = 0
            self._dead = True
        else:
            self._death_fails = new_value

    @property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, new_value: int):
        if new_value < 0:
            new_value = 0
        elif new_value > self.max_hp:
            new_value = int(self.max_hp)
        self._current_hp = new_value

    @property
    def dexterity(self):
        return self._dexterity

    @dexterity.setter
    def dexterity(self, new_value):
        self._dexterity = new_value
        self.armor_class = self.baseArmorClass
        for item in self.inventory:
            self.applyArmorClass(item)

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

        if new_class is None:
            return

        self.class_name = new_class["name"]
        self.class_index = new_class["index"]
        self.hd = new_class["hit_die"]
        self._class_levels = SRD_class_levels[self.class_index]
        if "spellcasting" in new_class:
            self.spellcasting_stat = new_class["spellcasting"]["spellcasting_ability"][
                "index"
            ]
        else:
            self.spellcasting_stat = None
        self.applyClassLevel()

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

        starting_equipment = new_class["starting_equipment"]
        for item in starting_equipment:
            for i in range(item["quantity"]):
                self.giveItem(SRD(item["equipment"]["url"]))

        self.player_options["starting_equipment"] = []

        def add_to_starting_options(choice: str):
            self.player_options["starting_equipment"].append(choice)

        def fetch_choices_string(option):
            choices = SRD(option["equipment_category"]["url"])["equipment"]
            choices_names = [c["name"] for c in choices]
            return "{} (choice from {})".format(
                option["equipment_category"]["name"], ", ".join(choices_names)
            )

        for item_option in new_class["starting_equipment_options"]:
            options = []
            opts = item_option["from"]
            if "options" not in opts.keys():
                choices = fetch_choices_string(opts)
                add_to_starting_options(choices)

            else:
                for opt in opts["options"]:
                    opt_type = opt["option_type"]
                    if opt_type == "counted_reference":
                        options.append(
                            "{} x {}".format(opt["count"], opt["of"]["name"])
                        )
                    elif opt_type == "choice":
                        how_many = opt["choice"]["choose"]
                        choices = fetch_choices_string(opt["choice"]["from"])
                        options.append("{} x {}".format(how_many, choices))
                    elif opt_type == "multiple":
                        try:
                            combo = [
                                str(c["count"]) + " " + c["of"]["name"]
                                for c in opt["items"]
                            ]
                            add_to_starting_options("{}".format(", ".join(combo)))
                        except KeyError:
                            # shield or martial weapon
                            martial_weapons = fetch_choices_string(
                                opt["items"][0]["choice"]["from"]
                            )
                            shield = opt["items"][1]["of"]["name"]
                            add_to_starting_options(
                                "choose 1 from {} or a {}".format(
                                    martial_weapons, shield
                                )
                            )
                            continue

                add_to_starting_options("choose from {}".format(", ".join(options)))

    def applyClassLevel(self):
        if self.level > 20:
            return
        for data in self._class_levels:
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
        if self.current_hp == self.max_hp:
            self.current_hp = Character.maximum_hp(
                self.hd, new_level, self.constitution
            )
        self.max_hp = Character.maximum_hp(self.hd, new_level, self.constitution)
        if self.current_hd == self.max_hd:
            self.current_hd = new_level
        self.max_hd = new_level
        if self.current_hd > self.max_hd:
            self.current_hd = self.max_hd
        self.applyClassLevel()

    def removeShields(self):
        """Removes all shields from self.inventory. Used by self.giveItem when equipping shield"""
        for i, item in enumerate(self.inventory):
            if (
                item["equipment_category"]["index"] == "armor"
                and item["armor_category"] == "Shield"
            ):
                self.inventory.pop(i)

    def removeArmor(self):
        """Removes all armor from self.inventory. Used by self.giveItem when equipping armor"""
        for i, item in enumerate(self.inventory):
            if (
                item["equipment_category"]["index"] == "armor"
                and item["armor_category"] != "Shield"
            ):
                self.inventory.pop(i)

    def applyArmorClass(self, item: dict):
        if item["equipment_category"]["index"] == "armor":
            if item["armor_category"] == "Shield":
                self.removeShields()
                try:
                    self.armor_class += item["armor_class"]["base"]
                except AttributeError:
                    # shield during __init__ without armor
                    self.armor_class = (
                        10
                        + item["armor_class"]["base"]
                        + Character.getModifier(self.dexterity)
                    )
            else:
                self.removeArmor()
                self.armor_class = item["armor_class"]["base"] + (
                    0
                    if not item["armor_class"]["dex_bonus"]
                    else Character.getModifier(self.dexterity)
                )

    @property
    def baseArmorClass(self):
        return 10 + Character.getModifier(self.dexterity)

    def giveItem(self, item: dict):
        """
        Adds an item to the Character's inventory list, as a dictionary.
        If the item is armor or a shield, the armor_class attribute will be set
        and any other armor/shields in the inventory will be removed.
        """
        self.applyArmorClass(item)

        self.inventory.append(item)

    def removeItem(self, item):
        if item["equipment_category"]["index"] == "armor":
            if item["armor_category"] == "Shield":
                self.armor_class -= item["armor_class"]["base"]
            else:
                extra_ac_bonus = 0
                shield = [
                    item
                    for item in self.inventory
                    if item["equipment_category"]["index"] == "armor"
                    and item["armor_category"] == "Shield"
                ]
                if shield:
                    extra_ac_bonus = shield[0]["armor_class"]["base"]
                self.armor_class = (
                    10 + extra_ac_bonus + Character.getModifier(self.dexterity)
                )

        self.inventory.remove(item)

    def giveWealth(self, amount) -> None:
        """
        Give wealth to character
        """
        self.wealth += amount

    def removeWealth(self, amount: int) -> bool:
        """
        Remove wealth from character if possible. Returns bool to indicate success or failure.
        If wealth < amount then wealth remains unchanged, otherwise this character loses wealth
        """
        if amount > self.wealth:
            return False
        else:
            self.wealth -= amount
            return True

    @staticmethod
    def setInitialAbilityScore(stat: Optional[int]) -> int:
        """
        Set ability score to an int. If the argument is None, then this method
        instead rolls for the initial starting ability score.
        """
        if stat is None:
            return sum_rolls(d6=4, drop_lowest=True)  # roll 4d6, drop lowest
        else:
            return int(stat)

    @staticmethod
    def getModifier(number: int) -> int:
        """
        This method returns the modifier for the given stat (INT, CON, etc.)
        The formula for this is (STAT - 10 / 2) so e.g. 14 results in 2
        """
        return math.floor((number - 10) / 2)

    @classmethod
    def maximum_hp(cls, hd: int, level: int, constitution: int) -> int:
        """
        Calculate maximum hitpoints using hit dice (HD), level and constitution modifier
        """
        return hd + ((int(hd / 2) + 1) * (level - 1)) + cls.getModifier(constitution)
