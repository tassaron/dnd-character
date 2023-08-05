from dnd_character import Character
from dnd_character.classes import CLASSES, Fighter
from dnd_character.experience import experience_at_level


thor = Character(
    name="Thor Odinson",
    age="34",
    level=1,
    gender="Male",
    description="Looks like a pirate angel",
    background="Born on Asgard, God of Thunder",
    classs=CLASSES["fighter"],
)

# Or you can use the class name as a function:
another_fighter = Fighter(name="Thor's Friend")

# See! They are both Fighters
assert thor.class_features == another_fighter.class_features

# Now that Thor is created, let's display the character in terminal
print(str(thor))

# Let's see what Thor looks like as a level 2
thor.experience += 300
print("Thor at level 2:")
print(f"New Level: {str(thor.level)}")
print(f"Current Experience: {str(thor.experience)}")
print(f"EXP to next Level: {str(thor.experience.to_next_level)}")

print()
thor.experience = experience_at_level(5)
print("Setting experience to level 5:")
print(f"New Level: {str(thor.level)}")
print(f"Current Experience: {str(thor.experience)}")
print(f"EXP to next Level: {str(thor.experience.to_next_level)}")

print()
thor.experience -= 1
print("Reducing experience by 1:")
print(f"New Level: {str(thor.level)}")
print(f"Current Experience: {str(thor.experience)}")
print(f"EXP to next Level: {str(thor.experience.to_next_level)}")

print("\nThor's class features at level 20: ")
thor.experience = experience_at_level(20)
print(", ".join([feat["name"] for feat in thor.class_features.values()]))
