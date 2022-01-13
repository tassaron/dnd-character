from setuptools import setup, find_packages
from os import path
from dnd_character.__init__ import __version__, __author__, __credits__

try:
    with open(
        path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = "missing README.md"

setup(
    name="dnd_character",
    author=__author__,
    credits=__credits__,
    packages=find_packages(),
    include_package_data=True,
    version=__version__,
    url="https://github.com/tassaron/dnd-character",
    license="EPL-2.0",
    description="make Dungeons & Dragons characters as serializable objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dnd trpg tabletop rpg",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
    ],
    # requests is needed in development to update the json_cache
    # install_requires=["requests"],
)
