import argparse


def main():
  parser = argparse.ArgumentParser(
    prog="dnd-character",
    description="generate D&D 5e character sheet as a text file from terminal"
  )
  parser.add_argument("-r", "--random", help="generate a random character", default=False, action="store_true")
  args = parser.parse_args()

  if args.random:
    import random
    from dnd_character.character import Character
    from dnd_character.classes import CLASSES
    classs = random.choice(list(CLASSES.keys()))
    char = Character(classs=CLASSES[classs])

    print(char)

main()
