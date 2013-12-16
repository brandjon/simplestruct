# Vector class that stores its magnitude.

from simplestruct import Struct, Field

class Vector(Struct):
    vals = Field(int, 'seq')
    mag = Field(float, '!')
    def __init__(self, vals):
        self.mag = sum(v ** 2 for v in vals) ** .5

v = Vector([1, 2, 5, 10])
print(v.mag)
