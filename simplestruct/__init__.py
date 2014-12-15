"""Provides a mechanism for defining classes with a fixed number of
fields, possibly type-checked and immutable. Methods are provided for
pretty-printing, equality testing, and hashing.
"""

__version__ = '0.1.0'

from .struct import *
from .fields import *
