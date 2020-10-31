from dnd_character import Character


if __name__ == "__main__":

    newCharacter = Character(
        name="Thor Odinson",
        age="34",
        gender="Male",
        description="Looks like a pirate angel",
        biography="Born on Asgard, God of Thunder",
    )

    # newCharacter is created, lets display some stats
    print(str(newCharacter))

    # Lets see what Thor looks like as a level 2
    newCharacter.giveExp(1000)
    print("Thor at level 2:")
    print(
        "New Level: " + str(newCharacter.level)
    )  # newCharacter.level is automatically increased when XP threshold increases
    print(
        "Current Experience: " + str(newCharacter.experience)
    )  # Current, experience after leveling up
    print(
        "EXP to next Level: " + str(newCharacter.nextLvlExperience)
    )  # 3000 Experience is required to get to level 3
