from dnd_character.equipment import Item, SRD_equipment


def test_all_items():
    """Constructs all 237 monsters from the SRD - we are now encumbered"""
    for item in SRD_equipment:
        assert Item(item).name == SRD_equipment[item]["name"]
