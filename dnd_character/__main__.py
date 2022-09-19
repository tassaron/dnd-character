import argparse
from dnd_character.character import Character
from dnd_character.classes import CLASSES
CLASS_NAMES = list(CLASSES.keys())

def main():
  parser = argparse.ArgumentParser(
    prog="dnd-character",
    description="generate D&D 5e character sheet as a text file from terminal"
  )
  actions = parser.add_mutually_exclusive_group()
  actions.add_argument("-r", "--random", help="generate a random character", default=False, action="store_true")
  actions.add_argument("-c", "--class", help="generate a character with specified class", nargs=1, choices=CLASS_NAMES)
  args = parser.parse_args()
  char = None

  if args.random:
    import random
    classs = random.choice(CLASS_NAMES)
    char = Character(classs=CLASSES[classs])

  # do gymnastics because class is a four letter word
  if args.__dict__["class"]:
    classs = args.__dict__["class"][0]
    char = Character(classs=CLASSES[classs])

  if char:
    print(char)
  else:
    parser.print_help()

main()
