"""Provides a mechanism for defining struct-like classes. These are
similar to collections.namedtuple classes but support optional type-
checking, mutability, and inheritance.
"""

__version__ = '0.2.3-dev'

from .struct import *
from .fields import *
