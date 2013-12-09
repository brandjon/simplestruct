from simplestruct import Struct, Field

class PointA:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointB(Struct):
    x = Field(int)
    y = Field(int)

pa1 = PointA(1, 2)
pa2 = PointA(1, 2)
print((pa1, pa2))
print(pa1 == pa2)
print((hash(pa1), hash(pa2)))

print()

pb1 = PointB(1, 2)
pb2 = PointB(1, 2)
print((pb1, pb2))
print(pb1 == pb2)
print((hash(pb1), hash(pb2)))
