"""Illustrates more advanced features like inheritance, mutability,
and user-supplied constructors.
"""

from simplestruct import Struct, Field


# Default values on fields work exactly like default values for
# constructor arguments. This includes the restriction that
# a non-default argument cannot follow a default argument.

class AxisPoint(Struct):
    x = Field(default=0)
    y = Field(default=0)

print('==== Default values ====')
p1 = AxisPoint(x=2)
print(p1)           # AxisPoint(x=2, y=0)
p2 = AxisPoint(y=3)
print(p2)           # AxisPoint(x=0, y=3)


# Subclasses by default do not inherit fields, but this can
# be enabled with a class-level flag.

class Point2D(Struct):
    x = Field
    y = Field

class Point3D(Point2D):
    _inherit_fields = True
    z = Field

print('\n==== Inheritance ====')
p = Point3D(1, 2, 3)
print(p)            # Point3D(x=1, y=2, z=3)

# The flag must be redefined on each subclass that wants to
# inherit fields.

# The list of fields can be programmatically accessed via the
# _struct attribute.

print(p._struct)    # (<field object>, <field object>, <field object>)
print([f.name for f in p._struct])  # ['x', 'y', 'z']

# Equality does not hold on different types, even if they are
# in the same class hierarchy and share the same fields.

class Point3D_2(Point3D):
    _inherit_fields = True

p2 = Point3D_2(1, 2, 3)
print(p == p2)     # False


# Structs are immutable by default, but this can be disabled
# with a class-level flag.

class MutablePoint(Struct):
    _immutable = False
    x = Field
    y = Field

print('\n==== Mutability ====')
p = Point2D(1, 2)
try:
    p.x = 3
except AttributeError as e:
    print(e)
p = MutablePoint(1, 2)
p.x = 3
print(p)        # MutablePoint(3, 2)

# Mutable structs can't be hashed (analogous to Python lists, dicts, sets).
try:
    hash(p)
except TypeError as e:
    print(e)


# Like other classes, a Struct is free to define its own constructor.
# The arguments are the declared fields, in order of their declaration.
#
# Fields are initialized in __new__(). A subclass that overrides
# __new__() must call super().__new__() (not type.__new__()).
# __init__() does not need to call super().__init__() or do any work
# on behalf of the Struct system.
#
# If the fields have default values, these are substituted in before
# calling the constructor. Thus providing default parameter values
# in the constructor argument list is meaningless, as they will always
# be overridden by the defaults from the field's declaration.

class DoublingVector2D(Struct):
    
    x = Field(default=0)
    y = Field(default=0)
    
    def __new__(cls, x, y):
        print('Vector2D.__new__() has been called')
        return super().__new__(cls, x, y)
    
    def __init__(self, x, y):
        # There is no need to call super().__init__().
        
        # The field values self.x and self.y have already been
        # initialized by __new__().
        
        # Before the call to __init__(), the instance attribute
        # _initialized is set to False. It is changed to True
        # once __init__() has finished executing. If there are
        # multiple __init__() calls chained via super(), it is
        # changed once the outermost call returns.
        
        assert not self._initialized
        
        # Despite the fact that this Struct is immutable, we
        # are free to reassign fields until the flag is set.
        # Likewise, we may not hash this instance until the
        # flag is set.
        
        self.x *= 2
        self.y *= 2
        try:
            hash(self)
        except TypeError as e:
            print(e) 
        
        # We can create additional non-field attributes.
        self.magnitude = (self.x**2 + self.y**2) ** .5
        # Since magnitude is not declared as a field, it is not
        # considered during equality comparison, hashing, pretty
        # printing, etc. Non-field attributes are generally
        # incidental to the value of the Struct, or else can be
        # deterministically derived from the fields. They can
        # be overwritten at any time, whether or not the Struct
        # is immutable.
        
        # Alternatively, We could define magnitude as a @property,
        # but then it would be recomputed each time it is used.

print('\n==== Custom constructor ====')
v = DoublingVector2D(1.5, 2)
print(v)            # DoublingVector2D(x=3, y=4)
print(v.magnitude)  # 5.0
