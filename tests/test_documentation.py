import sys
import re
import os


ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def get_code_blocks_from_markdown(markdown_filename: str):
    """
    Output code blocks from markdown file given a filename
    Modified code from Codeblocks https://github.com/shamrin/codeblocks
    """

    regex = re.compile(
        r"(?P<start>^```(?P<language>(\w|-)+)\n)(?P<code>.*?\n)(?P<end>```)",
        re.DOTALL | re.MULTILINE,
    )
    with open(markdown_filename, "r") as f:
        lines = [line for line in f]
    blocks = [
        (match.group("language"), match.group("code"))
        for match in regex.finditer("".join(lines))
    ]
    return [block for block_language, block in blocks if block_language == "python"]


def test_exec_readme_examples():
    """
    Simply tests that Python code blocks in the readme can be executed
    """
    markdown_python = get_code_blocks_from_markdown(os.path.join(ROOT_DIR, "README.md"))
    for section in markdown_python:
        exec(section)


def test_import_example_file():
    sys.path.insert(0, ROOT_DIR)

    # test that the example file is valid by importing it
    import example

    del sys.path[0]
