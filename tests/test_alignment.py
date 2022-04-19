import pytest
from dnd_character import Character


def test_alignment_is_2_characters():
    for length in (1, 3):
        with pytest.raises(AssertionError):
            new = Character(alignment="T" * length)


def test_alignment_is_uppercase():
    new = Character(alignment="cg")
    assert new.alignment == "CG"
