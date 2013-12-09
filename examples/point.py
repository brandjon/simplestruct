# Illustrates use of Struct to define a simple point class.

from simplestruct import Struct, Field

class PointA:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# The constructor is implicitly defined.
class PointB(Struct):
    x = Field(int)
    y = Field(int)

pa1 = PointA(1, 2)
pa2 = PointA(1, 2)

pb1 = PointB(1, 2)
pb2 = PointB(1, 2)

# Structs have pretty-printing.
print((pa1, pa2))
print((pb1, pb2))
print()

# Structs have structural equality (for like-typed objects).
print(pa1 == pa2)
print(pb1 == pb2)
print()

# ... with a corresponding hash function.
print((hash(pa1) == hash(pa2)))
print((hash(pb1) == hash(pb2)))
