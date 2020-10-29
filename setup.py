from setuptools import setup, find_packages
from os import path
from PyDnD.__init__ import __version__, __author__, __email__

try:
    with open(
        path.join(path.abspath(path.dirname(__file__)), "readme.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = "missing readme.md"

setup(
    name="PyDnD",
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    version=__version__,
    url="https://github.com/Coffee-fueled-deadlines/PyDnD",
    license="EPL-2.0",
    description="Python Dungeons and Dragons Library utilizing SRD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dnd trpg tabletop rpg",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
    ],
)
