import pytest
from dnd_character.character import Character, InvalidParameterError


def test_character_init_wealth_as_int():
    c = Character(wealth=100)
    assert c.wealth == 100.0


def test_character_init_wealth_detailed():
    c = Character(wealth_detailed={"pp": 0, "gp": 100, "ep": 0, "sp": 0, "cp": 0})
    assert c.wealth == 100.0


def test_character_init_wealth_matches_no_error():
    assert Character(
        wealth=100.0, wealth_detailed={"pp": 0, "gp": 100, "ep": 0, "sp": 0, "cp": 0}
    )


def test_character_init_wealth_mismatched_error():
    # Will fail if this exception is not raised
    with pytest.raises(InvalidParameterError):
        c = Character(
            wealth=10.0, wealth_detailed={"pp": 0, "gp": 100, "ep": 0, "sp": 0, "cp": 0}
        )


# Run this test with multiple inputs
@pytest.mark.parametrize(
    ("wealth_detailed", "expected_value"),
    (
        ({"pp": 0, "gp": 1, "ep": 0, "sp": 1, "cp": 1}, 1.11),
        ({"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1}, 2.11),
        ({"pp": 1, "gp": 0, "ep": 3, "sp": 0, "cp": 100}, 12.5),
        ({"pp": 0, "gp": 31, "ep": 0, "sp": 10, "cp": 9}, 32.09),
    ),
)
def test_wealth_calculated_from_detailed(wealth_detailed, expected_value):
    c = Character(wealth_detailed=wealth_detailed)
    assert c.wealth == expected_value


def test_character_increase_wealth_no_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 1, "cp": 1})
    c.change_wealth(sp=10, conversion=False)
    assert c.wealth_detailed == {"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1}


def test_character_increase_wealth_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 1, "cp": 1})
    c.change_wealth(sp=10, conversion=True)
    assert c.wealth_detailed == {"pp": 0, "gp": 2, "ep": 0, "sp": 1, "cp": 1}


def test_character_decrease_wealth_no_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1})
    c.change_wealth(pp=0, gp=-1, ep=0, sp=0, cp=0, conversion=False)
    assert c.wealth_detailed == {"pp": 0, "gp": 0, "ep": 0, "sp": 11, "cp": 1}


def test_character_decrease_wealth_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1})
    c.change_wealth(pp=0, gp=0, ep=0, sp=-20, cp=0, conversion=True)
    assert c.wealth_detailed == {"pp": 0, "gp": 0, "ep": 0, "sp": 1, "cp": 1}


def test_character_decrease_wealth_failure_no_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1})
    with pytest.raises(ValueError) as e:
        c.change_wealth(pp=0, gp=0, ep=0, sp=-20, cp=0, conversion=False)
        # make sure this is our ValueError, not somehow unrelated
        assert "not enough " in str(e)


def test_character_decrease_wealth_failure_conversion():
    c = Character(wealth_detailed={"pp": 0, "gp": 1, "ep": 0, "sp": 11, "cp": 1})
    with pytest.raises(ValueError) as e:
        c.change_wealth(pp=0, gp=0, ep=0, sp=-30, cp=0, conversion=True)
        # make sure this is our ValueError, not somehow unrelated
        assert "not enough " in str(e)


# Run this test with multiple inputs
@pytest.mark.parametrize(
    ("wealth", "inferred"),
    (
        (1.63, {"pp": 0, "gp": 1, "ep": 0, "sp": 6, "cp": 3}),
        (100.0, {"pp": 0, "gp": 100, "ep": 0, "sp": 0, "cp": 0}),
        (110.0, {"pp": 1, "gp": 100, "ep": 0, "sp": 0, "cp": 0}),
    ),
)
def test_infer_wealth(wealth, inferred):
    c = Character(wealth=wealth)
    assert c.wealth_detailed == inferred
