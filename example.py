from dnd_character import Character
from dnd_character import Roll


if __name__ == "__main__":

    newCharacter = Character(
        name="Thor Odinson",
        age="34",
        gender="Male",
        description="Looks like a pirate angel",
        biography="Born on Asgard, God of Thunder",
    )

    # newCharacter is created, lets display some stats
    print("Name:" + newCharacter.name)
    print("Age: " + newCharacter.age)
    print("Gender:" + newCharacter.gender)
    print("Description: " + newCharacter.description)
    print("Biography: " + newCharacter.biography)

    print("\n")

    print(
        "Level: " + str(newCharacter.level)
    )  # Level isn't specified in creation, so level is 1
    print(
        "Current Experience: " + str(newCharacter.experience)
    )  # Level wasn't specified, so current xp is 0
    print(
        "EXP to next Level: " + str(newCharacter.nextLvlExperience)
    )  # 1000 Experience is required to get to level 2
    print("\n\n\n")
    # Lets see what Thor looks like as a level 2

    newCharacter.giveExp(1000)
    print(
        "New Level: " + str(newCharacter.level)
    )  # newCharacter.level is automatically increased when XP threshold increases
    print(
        "Current Experience: " + str(newCharacter.experience)
    )  # Current, experience after leveling up
    print(
        "EXP to next Level: " + str(newCharacter.nextLvlExperience)
    )  # 3000 Experience is required to get to level 3
