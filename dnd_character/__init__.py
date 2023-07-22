"""
dnd-character is a Python package for integrating D&D 5e characters
into external applications. The character data is serializable so it
can be stored as json or a Python dict.
"""
from .character import Character  # noqa: F401, F405 (ignore unused import)
from .classes import *  # noqa: F401, F403 (ignore star import)

__author__ = "Brianna Rainey"
__copyright__ = "Copyright 2019-2023 Brianna Rainey & Markis Cook"
__credits__ = ["Brianna Rainey (Current Programmer)", "Markis Cook (Original Creator)"]
__license__ = "EPL-2.0"
__version__ = "23.07.22"
__maintainer__ = "Brianna Rainey"
