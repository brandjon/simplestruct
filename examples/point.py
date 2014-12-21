"""Illustrates the use of Struct classes, and their differences
from normal classes and namedtuples.
"""

from collections import namedtuple
from simplestruct import Struct, Field


###############################################################################
# Definition                                                                  #
###############################################################################

# Standard Python class.
class PyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Struct class.
class SPoint(Struct):
    # Field declaration order matters.
    x = Field   # shorthand for "x = Field()"
    y = Field
    # The constructor is implicitly defined.

# namedtuple class
NTPoint = namedtuple('NTPoint', 'x y')


###############################################################################
# Construction and pretty-printing                                            #
###############################################################################

# Initialization is the same for all three classes.
py_point = PyPoint(1, 2)
struct_point = SPoint(1, 2)
tuple_point = NTPoint(1, 2)

# Structs and namedtuples both have pretty-printing.
print('==== Printing ====')
print(py_point)         # <__main__.Pypoint object at ...>
print(struct_point)     # SPoint(x=1, y=2)
print(tuple_point)      # NTPoint(x=1, y=2)

# Structs print their contents using whichever formatting method
# was called originally. namedtuples always use repr.
struct_point2 = SPoint('a', 'b')
tuple_point2 = NTPoint('a', 'b')
print(str(struct_point2))        # SPoint(a, b)
print(repr(struct_point2))       # SPoint('a', 'b')
print(str(tuple_point2))         # NTPoint('a', 'b')
print(repr(tuple_point2))        # NTPoint('a', 'b')

# All three classes can also be constructed using
# keywords, *args, and **kargs.
py_point2 = PyPoint(1, y=2)
struct_point2 = SPoint(*[1, 2])
tuple_point2 = NTPoint(**{'x': 1, 'y': 2})


###############################################################################
# Equality and hashing                                                        #
###############################################################################

# Structs and namedtuples both have structural equality.
print('\n==== Equality ====')
print(py_point == py_point2)            # False
print(struct_point == struct_point2)    # True
print(tuple_point == tuple_point2)      # True

# Structs, unlike namedtuple, are only equal to other
# instances of the same class.
class OtherSPoint(Struct):
    x, y = Field, Field
OtherNTPoint = namedtuple('OtherNTPoint', 'x y')
struct_point2 = OtherSPoint(1, 2)
tuple_point2 = OtherNTPoint(1, 2)
print(struct_point == struct_point2)    # False
print(tuple_point == tuple_point2)      # True

# Structs and namedtuples have hash functions based on
# structural value.
print('\n==== Hashing ====')
print(hash(py_point) == hash(py_point2))        # False (almost certainly)
print(hash(struct_point) == hash(struct_point)) # True
print(hash(tuple_point) == hash(tuple_point2))  # True


###############################################################################
# Other features                                                              #
###############################################################################

# Structs implement some of the same convenience methods as namedtuples.
print('\n==== Convenience methods ====')
print(struct_point._asdict())       # OrderedDict([('x', 1), ('y', 2)])
print(tuple_point._asdict())        # OrderedDict([('x', 1), ('y', 2)])
print(struct_point._replace(x=3))   # SPoint(x=3, y=2)
print(tuple_point._replace(x=3))    # NTPoint(x=3, y=2)
# Note that _replace() creates a copy without modifying the original object.

# Both can be iterated over and decomposed into their components.
print(len(struct_point))    # 2
x, y = struct_point
print((x, y))               # (1, 2)
print(len(tuple_point))     # 2
x, y = tuple_point
print((x, y))               # (1, 2)
