"""Illustrates inheritance, non-field data, and mutability."""

from simplestruct import Struct, Field

class Point2D(Struct):
    x = Field
    y = Field

# Derived class that adds a computed magnitude data.
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

# Structs are immutable by default.
try:
    p1.x = 7
except AttributeError:
    print('Exception')

# Let's make a mutable 3D point. 
class Point3D(Point2D):
    _inherit_fields = True
    _immutable = False
    z = Field

p2 = Point3D(3, 4, 5)
print(p2)       # Point3D(x=3, y=4, z=5)
p2.x = 7
print(p2)       # Point3D(x=7, y=4, z=5)

try:
    hash(p2)
except TypeError:
    print('Exception')
