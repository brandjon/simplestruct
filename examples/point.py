"""Illustrates the use of Struct classes and their differences
from normal classes.
"""

from simplestruct import Struct, Field, TypedField

# Standard Python class.
class PointA:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Struct class.
class PointB(Struct):
    # Field declaration order matters.
    x = Field
    y = Field
    # The constructor is implicitly defined.

# Initialization is the same for both.
# Keywords, *args, and *kargs are allowed.
pa1 = PointA(1, 2)
pa2 = PointA(1, y=2)
pb1 = PointB(*[1, 2])
pb2 = PointB(**{'x': 1, 'y': 2})

# Structs have pretty-printing.
print('==== Printing ====')
print(pa1)  # <__main__.PointA object at ...>
print(pb1)  # PointB(x=1, y=2)

# Structs have structural equality (for like-typed objects)...
print('\n==== Equality ====')
print(pa1 == pa2)   # False
print(pb1 == pb2)   # True
print(pa1 == pb1)   # False

# ... with a corresponding hash function.
print('\n==== Hashing ====')
print((hash(pa1) == hash(pa2)))     # False (almost certainly)
print((hash(pb1) == hash(pb2)))     # True

# Struct with typed fields.
class TypedPoint(Struct):
    x = TypedField(int)
    y = TypedField(int)

print('\n==== Type checking ====')
tp1 = TypedPoint(1, 2)
try:
    tp2 = TypedPoint(1, 'b')
except TypeError:
    print('Exception')
