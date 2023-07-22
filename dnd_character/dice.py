import random


def sum_rolls(
    *,  # Force caller to use keyword arguments
    d100: int = 0,
    d20: int = 0,
    d12: int = 0,
    d10: int = 0,
    d8: int = 0,
    d6: int = 0,
    d4: int = 0,
    drop_lowest: bool = False,
):
    """Expected use: attack calculation, initial ability score, etc."""
    rolls = [random.randint(1, 100) for _ in range(d100)]
    rolls += [random.randint(1, 20) for _ in range(d20)]
    rolls += [random.randint(1, 12) for _ in range(d12)]
    rolls += [random.randint(1, 10) for _ in range(d10)]
    rolls += [random.randint(1, 8) for _ in range(d8)]
    rolls += [random.randint(1, 6) for _ in range(d6)]
    rolls += [random.randint(1, 4) for _ in range(d4)]

    if drop_lowest:
        rolls = sorted(rolls)[1:]

    return sum(rolls)


def roll_with_advantage_disadvantage(
    dice: int = 20, advantage: bool = False, disadvantage: bool = False
):
    """Expected use: D20 (ability checks, saving throws, attack rolls)"""
    if advantage == disadvantage:
        result = random.randint(1, dice)
    else:
        rolls = [random.randint(1, dice) for _ in range(2)]
        result = max(rolls) if advantage else min(rolls)
    return result
