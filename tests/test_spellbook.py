from dnd_character.spellbook import Spellbook
from dnd_character.classes import Wizard

# Initialize a Spellbook object
my_spellbook = Spellbook(contents=[], cost={}, desc=[], index="", name="", properties=[], special=[], url="",
                         equipment_category={})

lvl_1_wizard = Wizard(
    name="Level 1 Wizard ",
    level=1,
    wealth=75
)
lvl_3_wizard = Wizard(
    name="Level 3 Wizard ",
    level=3,
    wealth=750
)
lvl_5_wizard = Wizard(
    name="Level 3 Wizard ",
    level=5,
    wealth=700
)
lvl_7_wizard = Wizard(
    name="Level 7 Wizard ",
    level=7,
    wealth=100
)


def run_tests():
    # Create mock spell objects
    level_2_spell = type('Spell', (object,), {'level': 2, 'name': 'acid-arrow'})
    nonwizard_spell = type('Spell', (object,), {'level': 2, 'name': 'Animal Friendship'})
    level_3_spell = type('Spell', (object,), {'level': 3, 'name': 'Fireball'})
    mock_spell4 = type('Spell', (object,), {'level': 3, 'name': 'Vampiric Touch'})

    # Test Case 1: Level 1 Wizard tries to add a Level 2 spell (Should fail)
    result1 = my_spellbook.validate_spell(spell=level_2_spell, char_instance=lvl_1_wizard)
    assert result1 == False, "Test Case 1 Failed"

    # Test Case 2: Level 3 Wizard tries to add a Level 1 spell not in wizard spell list (Should fail)
    result2 = my_spellbook.validate_spell(spell=nonwizard_spell, char_instance=lvl_3_wizard)
    assert result2 == False, "Test Case 2 Failed"

    # Test Case 3: Level 5 Wizard tries to add a Level 3 spell in wizard spell list (Should pass)
    result3 = my_spellbook.validate_spell(spell=level_3_spell, char_instance=lvl_5_wizard)
    assert result3 == True, "Test Case 3 Failed"

    # Test Case 4: Level 5 tries to add a Level 3 spell but does not have enough gold (Should fail)
    result4 = my_spellbook.validate_spell(spell=mock_spell4, char_instance=lvl_7_wizard)
    assert result4 == False, "Test Case 4 Failed"

    print("All test cases passed!")


# Run the tests
run_tests()
