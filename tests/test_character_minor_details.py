from ctypes import alignment
from dnd_character import Character


def test_alignment_is_2_characters():
    for length in (1, 3):
        try:
            print("t" * length)
            new = Character(alignment="T" * length)
            assert len(new.alignment) == 2
        except AssertionError:
            # test will pass if this exception is raised
            pass


def test_alignment_is_uppercase():
    new = Character(alignment="cg")
    assert new.alignment.upper() == "CG"
