"""Illustrates more advanced features like type-checking,
inheritance, non-field data, and mutability.
"""

from simplestruct import Struct, Field, TypedField


print('==== Default values ====')

class AxisPoint(Struct):
    x = Field(default=0)
    y = Field(default=0)

p1 = AxisPoint(x=2)
print(p1)           # AxisPoint(x=2, y=0)
p2 = AxisPoint(y=3)
print(p2)           # AxisPoint(x=0, y=3)


print('\n==== Type checking ====')

class Point2D(Struct):
    x = TypedField(int)
    y = TypedField(int)

p1 = Point2D(2, 3)
try:
    Point2D('a', 'b')
except TypeError:
    print('Exception')


print('\n==== Mutability ====')

# Structs are immutable by default.
try:
    p1.x = 7
except AttributeError:
    print('Exception')

class Point3D(Point2D):
    _immutable = False
    x = Field
    y = Field
    z = Field

p2 = Point3D(3, 4, 5)
print(p2)       # Point3D(x=3, y=4, z=5)
p2.x = 7
print(p2)       # Point3D(x=7, y=4, z=5)

# Mutable structs can't be hashed (analogous to Python lists, dicts, sets).
try:
    hash(p2)
except TypeError:
    print('Exception')


print('\n==== Subclassing and non-field data ====')

class Vector2D(Point2D):
    # Special flag to inherit x and y fields without
    # needing to redeclare.
    _inherit_fields = True
    
    # Constructor takes in the field values.
    def __init__(self, x, y):
        # mag is not a field for the purposes of pretty printing,
        # equality comparison, etc. It could alternatively be
        # implemented as a @property.
        self.mag = (x**2 + y**2) ** .5
        
        # self.x and self.y are already automatically initialized,
        # but can be modified in __init__(), even though this
        # Struct is immutable. Be careful not to hash self until
        # after __init__() is done.
        
        # No need to call super().__init__().

p1 = Point2D(3, 4)
v1 = Vector2D(3, 4)
print(p1)       # Point2D(x=3, y=4)
print(v1)       # Vector2D(x=3, y=4)
print(v1.mag)   # 5.0
# Equality does not hold between different types.
print(p1 == v1) # False


print('\n==== More advanced types ====')

# n-dimensional vector
class Vector(Struct):
    # 'seq' is for sequence types. The value gets normalized
    # to a tuple.
    vals = TypedField(int, seq=True)

v1 = Vector([1, 2, 3, 4])
print(v1.vals)  # (1, 2, 3, 4)
