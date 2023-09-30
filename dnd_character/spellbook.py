from dnd_character.equipment import _Item
from .SRD import SRD
import requests
import json
import os

#Spellbook is a subclass of the _Item class that only accepts wizard spells as contents 
class Spellbook(_Item):
    # Constructor for initializing a new Spellbook instance
    def __init__(self, contents, cost, desc, index, name, properties, special, url, equipment_category, *args,
                 **kwargs):
        super().__init__(contents=contents, cost=cost, desc=desc, index=index, name=name, properties=properties,
                         special=special, url=url, equipment_category=equipment_category, *args, **kwargs)
        self.type = 'Spellbook'

    # Method to add a spell to the spellbook if it passes validation
    def add_spell(self, spell):
        if self.validate_spell(spell):
            self.contents.append(spell)
        else:
            print("Invalid spell. Only spells can be added to a spellbook.")

    # Method to validate a spell based on D&D wizard spellcasting rules
    def validate_spell(self, spell, spell_level=None, wizard_level=None, wizard_subclass=None):
        # Fetch the list of wizard spells by level from the SRD data
        wizard_spells_by_level = fetch_wizard_spells_from_json()

        # Check if the spell level exists in the dictionary
        if spell.level not in wizard_spells_by_level:
            print(f"Spell level {spell.level} not found in wizard spell list.")
            return False

        # Check if the spell is of a level the wizard can cast
        if spell.level > max_level_for_wizard(wizard_level):
            return False

        # Check if the spell is in the wizard spell list
        if spell.name not in wizard_spells_by_level[spell.level]:
            return False

        # Optional: Check for subclass or component restrictions
        if wizard_subclass and not is_spell_allowed_for_subclass(spell, wizard_subclass):
            return False

        return True


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

#Function to retrieve the wizard spell data from the JSON cache
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

        return wizard_spells_by_level

    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

    wizard_spells_by_level = {}
    try:
        with open(json_cache_path, 'r') as f:  # Use json_cache_path instead of json_file_path
            spells = json.load(f)["results"]
        for spell in spells:
            spell_data_path = os.path.join(current_script_path, 'json_cache', f"api_spells_{spell['index']}.json")
            print(f"Attempting to open additional JSON file at {spell_data_path}...")
            try:
                with open(spell_data_path, 'r') as f:
                    spell_data = json.load(f)
                    print("Additional JSON file read successfully. Content:", spell_data)
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
        return wizard_spells_by_level
    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

# Initialize a Spellbook object
my_spellbook = Spellbook(contents=[], cost={}, desc=[], index="", name="", properties=[], special=[], url="", equipment_category={})


def run_tests():
    # Create mock spell objects
    mock_spell1 = type('Spell', (object,), {'level': 2, 'name': 'MockSpell1'})
    mock_spell2 = type('Spell', (object,), {'level': 2, 'name': 'NonWizardSpell'})
    mock_spell3 = type('Spell', (object,), {'level': 3, 'name': 'Fireball'})
    mock_spell4 = type('Spell', (object,), {'level': 3, 'name': 'VampiricTouch'})

    # Test Case 1: Level 1 Wizard tries to add a Level 2 spell (Should fail)
    result1 = my_spellbook.validate_spell(spell=mock_spell1, wizard_level=1)
    assert result1 == False, "Test Case 1 Failed"

    # Test Case 2: Level 3 Wizard tries to add a Level 2 spell not in wizard spell list (Should fail)
    result2 = my_spellbook.validate_spell(spell=mock_spell2, wizard_level=3)
    assert result2 == False, "Test Case 2 Failed"

    # Test Case 3: Level 5 Wizard tries to add a Level 3 spell in wizard spell list (Should pass)
    result3 = my_spellbook.validate_spell(spell=mock_spell3, wizard_level=5)
    assert result3 == True, "Test Case 3 Failed"

    # Test Case 4: Level 5 Wizard of subclass 'Evocation' tries to add a Level 3 spell restricted to 'Necromancy' (Should fail)
    result4 = my_spellbook.validate_spell(spell=mock_spell4, wizard_level=5, wizard_subclass="Evocation")
    assert result4 == False, "Test Case 4 Failed"

    print("All test cases passed!")


# Run the tests
#run_tests()
