import dnd_character.character
from dnd_character.equipment import _Item
from dnd_character import character
import json
import os
import dnd_character


# Spellbook is a subclass of the _Item class that only accepts wizard spells as contents
class Spellbook(_Item):
    # Constructor for initializing a new Spellbook instance
    MAX_SPELLS = 100  # Class variable to define the maximum number of spells

    def __init__(self, contents, cost, desc, index, name, properties, special, url, equipment_category, *args,
                 **kwargs):
        super().__init__(contents=contents, cost=cost, desc=desc, index=index, name=name, properties=properties,
                         special=special, url=url, equipment_category=equipment_category, *args, **kwargs)
        self.type = 'Spellbook'

    # Method to add a spell to the spellbook if it passes validation
    def add_spell(self, spell, char_instance):
        if len(self.contents) >= Spellbook.MAX_SPELLS:
            print("Spellbook is full. Cannot add more spells.")
            return

        if self.validate_spell(spell, char_instance):
            self.contents.append(spell)
        else:
            print("Invalid spell. Only spells can be added to a spellbook.")

    # Method to remove a spell from a spellbook
    def remove_spell(self, spell):
        if spell in self.contents:
            self.contents.remove(spell)
            print(f"Removed {spell} from the spellbook.")
        else:
            print(f"{spell} not found in the spellbook.")

    def check_components(self, char_instance, cost):
        print(char_instance.wealth)
        return char_instance.wealth >= cost

    # Method to validate a spell based on D&D wizard spellcasting rules
    def validate_spell(self, spell, char_instance):
        # Fetch the list of wizard spells by level from the SRD data
        wizard_spells_by_level = fetch_wizard_spells_from_json()
        print(f"Validating spell: {spell.name}, for character: {char_instance.name}")  # Print spell and character info
        # Check if character is a wizard
        if not char_instance.classs.name == "Wizard":
            print(f"{char_instance.name} is not a wizard and cannot scribe spells.")
            return False

        # Check if the spell level exists in the dictionary
        if spell.level not in wizard_spells_by_level:
            print(f"Spell level {spell.level} not found in wizard spell list.")
            return False

        # Check if the spell is of a level the wizard can cast
        if spell.level > max_level_for_wizard(char_instance.level):
            return False

        # Check if the spell is in the wizard spell list
        if spell.name not in wizard_spells_by_level[spell.level]:
            return False

        # Check for component restrictions
        cost = spell.level * 50 * dnd_character.character.coin_value['gp']
        cost_in_cp = cost * (1 / dnd_character.character.coin_value['gp']) * dnd_character.character.coin_value['cp']

        if not self.check_components(char_instance, cost):
            print(f"Insufficient gold to scribe {spell.name}.")
            return False
        print(f"Char detailed wealth before transaction: {char_instance.wealth_detailed}")  # Debug line
        print(f"Char wealth before transaction: {char_instance.wealth}")  # Debug line
        try:
            print(f"Cost of transaction: {cost}")  # Debug line
            char_instance.change_wealth(cp=-cost_in_cp)  # deduct cost
            print(f"Char detailed wealth after transaction: {char_instance.wealth_detailed}")  # New debug line
            return True
        except ValueError:  # Insufficient funds
            print("Exception occurred: ValueError - Insufficient funds")
            return False


def max_level_for_wizard(wizard_level):
    if wizard_level < 1:
        return 0  # Invalid wizard level
    elif wizard_level < 3:
        return 1  # Level 1 spells
    elif wizard_level < 5:
        return 2  # Level 2 spells
    elif wizard_level < 7:
        return 3  # Level 3 spells
    elif wizard_level < 9:
        return 4  # Level 4 spells
    elif wizard_level < 11:
        return 5  # Level 5 spells
    elif wizard_level < 13:
        return 6  # Level 6 spells
    elif wizard_level < 15:
        return 7  # Level 7 spells
    elif wizard_level < 17:
        return 8  # Level 8 spells
    else:
        return 9  # Level 9 spells


# Function to retrieve the wizard spell data from the JSON cache
def fetch_wizard_spells_from_json():
    current_script_path = os.path.dirname(__file__)
    json_cache_path = os.path.join(current_script_path, 'json_cache', 'api_spells.json')

    if not os.path.exists(json_cache_path):
        print("JSON file does not exist at the path.")
        return None

    wizard_spells_by_level = {}

    try:
        with open(json_cache_path, 'r') as f:
            spells = json.load(f)["results"]

        for spell in spells:
            spell_file_path = os.path.join(current_script_path, 'json_cache', f"api_spells_{spell['index']}.json")

            if not os.path.exists(spell_file_path):
                continue

            with open(spell_file_path, 'r') as spell_file:
                spell_data = json.load(spell_file)

            if 'wizard' in [cls['name'].lower() for cls in spell_data.get('classes', [])]:
                level = spell_data['level']
                wizard_spells_by_level.setdefault(level, []).append(spell_data['name'])

    except (FileNotFoundError, json.JSONDecodeError):
        print("Error encountered while processing JSON.")

    try:
        with open(json_cache_path, 'r') as f:
            spells = json.load(f)["results"]
        for spell in spells:
            spell_data_path = os.path.join(current_script_path, 'json_cache', f"api_spells_{spell['index']}.json")
            # print(f"Attempting to open additional JSON file at {spell_data_path}...")
            try:
                with open(spell_data_path, 'r') as f:
                    spell_data = json.load(f)
                    # print("Additional JSON file read successfully. Content:", spell_data)
            except FileNotFoundError:
                print(f"Additional JSON file {spell_data_path} not found.")
                continue
            except json.JSONDecodeError:
                print("Error decoding additional JSON file.")
                continue
            if 'wizard' in [cls['name'].lower() for cls in spell_data.get('classes', [])]:
                level = spell_data['level']
                if level not in wizard_spells_by_level:
                    wizard_spells_by_level[level] = []
                wizard_spells_by_level[level].append(spell_data['name'])
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error encountered while processing JSON.")

    return wizard_spells_by_level


