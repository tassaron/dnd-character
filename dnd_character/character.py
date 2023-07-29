from typing import Optional, Union, Iterator, TYPE_CHECKING
from uuid import uuid4, UUID
import logging

if TYPE_CHECKING:
    from .classes import _CLASS
    from .spellcasting import _SPELL

from .SRD import SRD, SRD_class_levels
from .equipment import _Item, Item
from .experience import Experience, experience_at_level, level_at_experience
from .dice import sum_rolls


LOG = logging.getLogger(__package__)

coin_value = {"pp": 10, "gp": 1, "ep": 0.5, "sp": 0.1, "cp": 0.01}


class InvalidParameterError(Exception):
    pass


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
        uid: Optional[Union[UUID, str]] = None,
        classs: Optional["_CLASS"] = None,
        class_name: Optional[str] = None,
        class_index: Optional[str] = None,
        name: Optional[str] = None,
        age: Optional[str] = None,
        gender: Optional[str] = None,
        species: Optional[str] = None,
        speed: Optional[int] = None,
        alignment: Optional[str] = None,
        description: Optional[str] = None,
        background: Optional[str] = None,
        personality: Optional[str] = None,
        ideals: Optional[str] = None,
        bonds: Optional[str] = None,
        flaws: Optional[str] = None,
        level: Optional[int] = None,
        experience: Union[int, None, Experience] = None,
        wealth: Optional[Union[int, float]] = None,
        wealth_detailed: Optional[dict] = None,
        strength: Optional[int] = None,
        dexterity: Optional[int] = None,
        constitution: Optional[int] = None,
        wisdom: Optional[int] = None,
        intelligence: Optional[int] = None,
        charisma: Optional[int] = None,
        max_hp: Optional[int] = None,
        current_hp: Optional[int] = None,
        temp_hp: Optional[int] = None,
        hd: int = 8,
        max_hd: Optional[int] = None,
        current_hd: Optional[int] = None,
        proficiencies: Optional[dict] = None,
        saving_throws: Optional[list] = None,
        cantrips_known: Optional[list["_SPELL"]] = None,
        spells_known: Optional[list["_SPELL"]] = None,
        spells_prepared: Optional[list["_SPELL"]] = None,
        spell_slots: Optional[dict[str, int]] = None,
        skills_strength: Optional[dict] = None,
        skills_dexterity: Optional[dict] = None,
        skills_wisdom: Optional[dict] = None,
        skills_intelligence: Optional[dict] = None,
        skills_charisma: Optional[dict] = None,
        inventory: Optional[list[dict]] = None,
        prof_bonus: int = 0,
        ability_score_bonus: int = 0,
        class_features: Optional[dict] = None,
        class_features_enabled: Optional[list] = None,
        spellcasting_stat: Optional[str] = None,
        player_options: Optional[dict] = None,
        armor_class: Optional[int] = None,
        death_saves: int = 0,
        death_fails: int = 0,
        exhaustion: int = 0,
        dead: bool = False,
        conditions: Optional[dict] = None,
    ):
        """
        Typical Arguments:
                name         (str)
                age          (str)
                gender       (str)
                alignment    (str): two letter alignment (LE, TN, CN, LG, etc.)
                description  (str): physical description of character
                background   (str): one-word backstory of character (e.g. knight, chef)
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
        self.uid: UUID = (
            uuid4() if uid is None else uid if isinstance(uid, UUID) else UUID(uid)
        )
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

        # Ability Scores
        self.strength = self.set_initial_ability_score(strength)
        self._dexterity = self.set_initial_ability_score(dexterity)
        self.constitution = self.set_initial_ability_score(constitution)
        self.wisdom = self.set_initial_ability_score(wisdom)
        self.intelligence = self.set_initial_ability_score(intelligence)
        self.charisma = self.set_initial_ability_score(charisma)

        # Hit Dice and Hit Points: self.hd == 8 is a d8, 10 is a d10, etc
        self.hd = 8 if hd is None else hd
        self.max_hd = 1 if max_hd is None else max_hd
        self.current_hd = 1 if current_hd is None else current_hd
        self.max_hp = (
            Character.get_maximum_hp(
                self.hd, 1 if level is None else int(level), self.constitution
            )
            if max_hp is None
            else max_hp
        )
        self._current_hp = current_hp if current_hp is not None else int(self.max_hp)
        self.temp_hp = 0 if temp_hp is None else int(temp_hp)

        # Spells, Skills, Proficiencies
        self.proficiencies = proficiencies if proficiencies is not None else {}
        self.saving_throws = saving_throws if saving_throws is not None else []
        self.spellcasting_stat = spellcasting_stat
        self._cantrips_known: list["_SPELL"] = (
            cantrips_known if cantrips_known is not None else []
        )
        self._spells_known: list["_SPELL"] = (
            spells_known if spells_known is not None else []
        )
        self._spells_prepared: list["_SPELL"] = (
            spells_prepared if spells_prepared is not None else []
        )
        self.set_spell_slots(spell_slots)

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
                self._experience._experience = experience_at_level(level)
                self._experience.update_level()
                # Experience alters self.level so it is now the correct value
            else:
                # if level is specified AND experience is not zero:
                # the Experience object normally handles the self.level attr
                # but if a user changes their level manually, it should override this anyway
                LOG.info(
                    f"Custom level for {str(self.name)}: {str(level)} instead of {str(self.level)}"
                )
                self._level = level

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
        final_wealth = None
        if wealth_detailed is None:
            final_wealth = float(sum_rolls(d10=4)) if wealth is None else wealth
            self.wealth_detailed = self.infer_wealth(final_wealth)
        else:
            self.wealth_detailed = wealth_detailed
            final_wealth = sum(
                [coin_value[u] * v for u, v in self.wealth_detailed.items()]
            )

        # if both wealth parameters provided
        if wealth is not None and float(wealth) != final_wealth:
            raise InvalidParameterError(
                "Both 'wealth' and 'wealth_detailed' parameters are provided, but 'wealth' seems incorrect."
            )
        self.wealth = final_wealth

        # Inventory. Deserialize items and give them one by one
        self._inventory: list[_Item] = []
        if inventory is not None:
            for item in inventory:
                self.give_item(_Item(**item))

        # Final steps of initialization -- the classs.setter does lots of work here
        # setting the self.classs attr applies "class features" appropriate to character's level
        self.classs = classs

        # base armor class is 10 + DEX; will be affected by inventory
        if armor_class is not None:
            self.armor_class = armor_class
        elif not hasattr(self, "armor_class"):
            self.armor_class = self.base_armor_class
        self._dead = dead
        self._death_saves = death_saves
        self._death_fails = death_fails
        self.exhaustion = exhaustion

        if self.level == level_at_experience(self._experience._experience):
            self.level = self._level
            if current_hp is None:
                # Set character's HP to the maximum for their level,
                # only if the level isn't custom! (if it matches experience points according to SRD)
                self.current_hp = Character.get_maximum_hp(
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
            self.conditions = {k: False for k in all_conditions}
        else:
            self.conditions = {
                k: conditions[k] if k in conditions.keys() else False
                for k in all_conditions
            }

    def __str__(self) -> str:
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
            f"Inventory:\n{', '.join([item.name for item in self.inventory])}\n\n"
            f"Class Features:\n{', '.join([item['name'] for item in self.class_features.values()])}\n\n"
        )

    def __iter__(self) -> Iterator[tuple[str, Union[dict, list, int, str, bool, None]]]:
        """
        Enables `dict(self)` to return a dictionary representation of this object.
        Iterate over this object to get (key, value) pairs.

        Attrs starting with _ are skipped, as we assume they are non-serializable.
        Such attrs must be added manually to the functions in this method.
        """

        def keys() -> list[str]:
            keys = [key for key in self.__dict__ if not key.startswith("_")]
            keys.extend(
                [
                    "experience",
                    "death_saves",
                    "death_fails",
                    "dexterity",
                    "dead",
                    "current_hp",
                    "inventory",
                    "cantrips_known",
                    "spells_known",
                    "spells_prepared",
                ]
            )
            return keys

        def values() -> list[Union[dict, list, int, str, bool, None]]:
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
                    [dict(item) for item in self._inventory],
                    [dict(spell) for spell in self._cantrips_known],
                    [dict(spell) for spell in self._spells_known],
                    [dict(spell) for spell in self._spells_prepared],
                ]
            )
            return vals

        return zip(keys(), values())

    def __repr__(self) -> str:
        """Returns a string that could be copy-pasted to create a new instance of this object"""
        quote = lambda value: "'" if type(value) is str else ""
        kwargs = [f"{key}={quote(value)}{value}{quote(value)}" for key, value in self]
        return f"{type(self).__name__}({', '.join(kwargs)})"

    def __eq__(self, other) -> bool:
        """
        Check if `other` is an identical character to `self`
        Or if `other` is a dict that would construct an identical character
        """
        if type(other) is dict:
            other = Character(**other)
        if not isinstance(other, type(self)):
            return False
        for pair1, pair2 in zip(self, other):
            if pair1 != pair2:
                return False
        return True

    @property
    def cantrips_known(self) -> list["_SPELL"]:
        return self._cantrips_known

    @cantrips_known.setter
    def cantrips_known(self, new_val) -> None:
        self._cantrips_known = new_val

    @property
    def spells_known(self) -> list["_SPELL"]:
        return self._spells_known

    @spells_known.setter
    def spells_known(self, new_val) -> None:
        self._spells_known = new_val

    @property
    def spells_prepared(self) -> list["_SPELL"]:
        return self._spells_prepared

    @spells_prepared.setter
    def spells_prepared(self, new_val) -> None:
        self._spells_prepared = new_val

    @property
    def inventory(self) -> list[_Item]:
        return self._inventory

    @property
    def dead(self) -> bool:
        return self._dead

    @dead.setter
    def dead(self, new_value: bool) -> None:
        self._dead = new_value
        self._death_saves = 0
        self._death_fails = 0

    @property
    def death_saves(self) -> int:
        return self._death_saves

    @death_saves.setter
    def death_saves(self, new_value: int) -> None:
        if not 4 > new_value > -1:
            raise ValueError("Death saving throws must be in range 0-3")
        elif new_value == 3:
            self._death_saves = 0
            self._death_fails = 0
            self._dead = False
        else:
            self._death_saves = new_value

    @property
    def death_fails(self) -> int:
        return self._death_fails

    @death_fails.setter
    def death_fails(self, new_value: int) -> None:
        if not 4 > new_value > -1:
            raise ValueError("Death saving throws must be in range 0-3")
        elif new_value == 3:
            self._death_saves = 0
            self._death_fails = 0
            self._dead = True
        else:
            self._death_fails = new_value

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, new_value: int) -> None:
        if new_value < 0:
            new_value = 0
        elif new_value > self.max_hp:
            new_value = int(self.max_hp)
        self._current_hp = new_value

    @property
    def dexterity(self) -> int:
        return self._dexterity

    @dexterity.setter
    def dexterity(self, new_value: int) -> None:
        self._dexterity = new_value
        self.armor_class = self.base_armor_class
        for item in self.inventory:
            self.apply_armor_class(item)

    @property
    def experience(self) -> Experience:
        return self._experience.experience

    @experience.setter
    def experience(self, new_val: int) -> None:
        if new_val is None:
            pass
        elif type(new_val) is Experience:
            self._experience = new_val
        else:
            self._experience._experience = new_val
            self._experience.update_level()

    @property
    def classs(self) -> Optional["_CLASS"]:
        return self.__class

    @classs.setter
    def classs(self, new_class: Optional["_CLASS"]) -> None:
        """
        Triggered when the character's class is changed
        """
        if isinstance(new_class, dict):
            # backwards compatibility
            from .classes import CLASSES

            LOG.warning("Implicitly converting classs dict to dataclass.")
            new_class = CLASSES[new_class["index"]]

        self.__class = new_class
        if new_class is None:
            return

        def set_class() -> None:
            """
            Set miscellaneous class-related properties such as:
            class name, hit dice, level progression data, proficiencies, saving throws,
            spellcasting, and class features
            """
            self.class_name = new_class.name
            self.class_index = new_class.index
            self.hd = new_class.hit_die
            self._class_levels = SRD_class_levels[self.class_index]
            if new_class.spellcasting:
                self.spellcasting_stat = new_class.spellcasting["spellcasting_ability"][
                    "index"
                ]
            else:
                self.spellcasting_stat = None
            self.apply_class_level()

            # create dict such as { "all-armor": {"name": "All armor", "type": "Armor"} }
            for proficiency in new_class.proficiencies:
                data = SRD(proficiency["url"])
                self.proficiencies[proficiency["index"]] = {
                    "name": data["name"],
                    "type": data["type"],
                }

            self.saving_throws = [
                saving_throw["name"] for saving_throw in new_class.saving_throws
            ]

        def set_starting_equipment() -> None:
            """
            Sets `player_options["starting_equipment"]` to a list of strings
            """
            for starting_equipment in new_class.starting_equipment:
                new_item = Item(starting_equipment["equipment"]["index"])
                new_item.quantity = starting_equipment["quantity"]
                self.give_item(new_item)

            self.player_options["starting_equipment"] = []

            def add_to_starting_options(choice: str) -> None:
                self.player_options["starting_equipment"].append(choice)

            def fetch_choices_string(option: dict[str, dict[str, str]]) -> str:
                choices = SRD(option["equipment_category"]["url"])["equipment"]
                choices_names = [c["name"] for c in choices]
                return "{} (choice from {})".format(
                    option["equipment_category"]["name"], ", ".join(choices_names)
                )

            for item_option in new_class.starting_equipment_options:
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

        set_class()
        set_starting_equipment()

    def apply_class_level(self) -> None:
        """
        Applies changes based on the character's class and level
        e.g., adds new class features, spell slots
        Called by `level.setter` and `classs.setter`
        """
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

            # Fetch new spell slots
            spell_slots = data.get("spellcasting", self.spell_slots)
            self.set_spell_slots(spell_slots)

    def set_spell_slots(self, new_spell_slots: dict[str, int]) -> dict[str, int]:
        default_spell_slots = {
            "cantrips_known": 0,
            "spells_known": 0,
            "spell_slots_level_1": 0,
            "spell_slots_level_2": 0,
            "spell_slots_level_3": 0,
            "spell_slots_level_4": 0,
            "spell_slots_level_5": 0,
            "spell_slots_level_6": 0,
            "spell_slots_level_7": 0,
            "spell_slots_level_8": 0,
            "spell_slots_level_9": 0,
        }
        self.spell_slots = new_spell_slots if new_spell_slots is not None else {}
        for key in default_spell_slots:
            if key not in self.spell_slots:
                self.spell_slots[key] = default_spell_slots[key]

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, new_level: int) -> None:
        self._level = new_level
        if self.current_hp == self.max_hp:
            self.current_hp = Character.get_maximum_hp(
                self.hd, new_level, self.constitution
            )
        self.max_hp = Character.get_maximum_hp(self.hd, new_level, self.constitution)
        if self.current_hd == self.max_hd:
            self.current_hd = new_level
        self.max_hd = new_level
        if self.current_hd > self.max_hd:
            self.current_hd = self.max_hd
        self.apply_class_level()

    def remove_shields(self) -> None:
        """Removes all shields from self._inventory. Used by self.give_item when equipping shield"""
        for i, item in enumerate(self._inventory):
            if (
                item.equipment_category["index"] == "armor"
                and item.armor_category == "Shield"
            ):
                self._inventory.pop(i)

    def remove_armor(self) -> None:
        """Removes all armor from self._inventory. Used by self.give_item when equipping armor"""
        for i, item in enumerate(self._inventory):
            if (
                item.equipment_category["index"] == "armor"
                and item.armor_category != "Shield"
            ):
                self._inventory.pop(i)

    def apply_armor_class(self, item: _Item) -> None:
        if item.equipment_category["index"] == "armor":
            if item.armor_category == "Shield":
                self.remove_shields()
                try:
                    self.armor_class += item.armor_class["base"]
                except AttributeError:
                    # shield during __init__ without armor
                    self.armor_class = (
                        10
                        + item.armor_class["base"]
                        + Character.get_ability_modifier(self.dexterity)
                    )
            else:
                self.remove_armor()
                self.armor_class = item.armor_class["base"] + (
                    0
                    if not item.armor_class["dex_bonus"]
                    else Character.get_ability_modifier(self.dexterity)
                )

    @property
    def base_armor_class(self) -> int:
        return 10 + Character.get_ability_modifier(self.dexterity)

    def give_item(self, item: _Item) -> None:
        """
        Adds an item to the Character's inventory list.
        If the item is armor or a shield, the armor_class attribute will be set
        and any other armor/shields in the inventory will be removed.
        """
        self.apply_armor_class(item)
        self.inventory.append(item)

    def remove_item(self, item: _Item) -> None:
        if item.equipment_category["index"] == "armor":
            if item.armor_category == "Shield":
                self.armor_class -= item.armor_class["base"]
            else:
                extra_ac_bonus = 0
                shield = [
                    item
                    for item in self._inventory
                    if item.equipment_category["index"] == "armor"
                    and item.armor_category == "Shield"
                ]
                if shield:
                    extra_ac_bonus = shield[0].armor_class["base"]
                self.armor_class = (
                    10 + extra_ac_bonus + Character.get_ability_modifier(self.dexterity)
                )

        self._inventory.remove(item)

    def change_wealth(
        self,
        pp: int = 0,
        gp: int = 0,
        ep: int = 0,
        sp: int = 0,
        cp: int = 0,
        conversion: bool = False,
    ) -> None:
        change = locals()
        change.pop("self", None)
        change.pop("conversion", None)

        total_change = sum([coin_value[u] * v for u, v in change.items()])
        new_wealth = round(self.wealth + total_change, 2)
        if new_wealth < 0:
            raise ValueError("Character has not enough wealth to cover the change!")

        if conversion:
            self.wealth_detailed = self.infer_wealth(new_wealth)
        else:
            for unit, value in change.items():
                new_value = self.wealth_detailed[unit] + value
                if new_value < 0:
                    raise ValueError(
                        f"Character has not enough {unit}! Current balance: {self.wealth_detailed[unit]}"
                    )
                self.wealth_detailed[unit] = new_value

        self.wealth = new_wealth

    @staticmethod
    def infer_wealth(wealth: Union[int, float]) -> dict[str, int]:
        """Estimates a reasonable coin distribution from gold denominated total wealth."""
        # Convert to platinum for smaller weight/volume
        if wealth > 100:
            pp = int((wealth - 100) / 10)
            gp = wealth - 10 * pp
        else:
            pp = 0
            gp = wealth

        # Convert fractional part to silver and copper (no electrum!)
        gp_str = "{:.2f}".format(gp)  # two decimal rounded gp to two decimal string
        gp_str_decimal = gp_str.split(".")[1]
        sp = int(gp_str_decimal[0])
        cp = int(gp_str_decimal[1])
        gp = int(gp)

        return {"pp": pp, "gp": gp, "ep": 0, "sp": sp, "cp": cp}

    @staticmethod
    def set_initial_ability_score(stat: Optional[int]) -> int:
        """
        Set ability score to an int. If the argument is None, then this method
        instead rolls for the initial starting ability score.
        """
        if stat is None:
            return sum_rolls(d6=4, drop_lowest=True)  # roll 4d6, drop lowest
        else:
            return int(stat)

    @staticmethod
    def get_ability_modifier(number: int) -> int:
        """
        This method returns the modifier for the given stat (INT, CON, etc.)
        The formula for this is (STAT - 10 / 2) so e.g. 14 results in 2
        """
        return (number - 10) // 2

    @staticmethod
    def get_maximum_hp(hd: int, level: int, constitution: int) -> int:
        """
        Calculate maximum hitpoints using hit dice (HD), level and constitution modifier
        """
        return (
            hd
            + ((int(hd / 2) + 1) * (level - 1))
            + Character.get_ability_modifier(constitution)
        )
