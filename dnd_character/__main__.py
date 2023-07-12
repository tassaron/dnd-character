import argparse
import json
from pprint import pprint
from dnd_character.character import Character
from dnd_character.classes import CLASSES

CLASS_NAMES = list(CLASSES.keys())


def main():
    parser = argparse.ArgumentParser(
        prog="dnd-character",
        description="generate D&D 5e character sheet from terminal",
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "-r",
        "--random",
        help="generate a random character",
        default=False,
        action="store_true",
    )
    actions.add_argument(
        "-c",
        "--class",
        help="generate a character with specified class",
        nargs=1,
        choices=CLASS_NAMES,
    )
    parser.add_argument(
        "-l",
        "--level",
        help="set character to level",
        default="1",
        choices=[str(i) for i in range(1, 21)],
    )
    parser.add_argument(
        "-f",
        "--format",
        help="output format",
        default="text",
        choices=["text", "dict", "json"],
    )
    args = parser.parse_args()
    char = None

    if args.random:
        import random

        classs = random.choice(CLASS_NAMES)
        char = Character(classs=CLASSES[classs], level=int(args.level))

    # do gymnastics because class is a four letter word
    if args.__dict__["class"]:
        classs = args.__dict__["class"][0]
        char = Character(classs=CLASSES[classs], level=int(args.level))

    if char:
        if args.format == "text":
            print(char)
        elif args.format == "dict":
            pprint(dict(char))
        elif args.format == "json":
            print(json.dumps(dict(char), indent=2))
    else:
        parser.print_help()


main()
