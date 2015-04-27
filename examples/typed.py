"""Shows use of type-checked fields."""

from numbers import Number
from simplestruct import Struct, Field, TypedField


# The standard abstract base class Number is handy because it
# lets us restrict TypedPoint to any of int, float, complex, etc.

class TypedPoint(Struct):
    x = TypedField(Number)
    y = TypedField(Number)

p = TypedPoint(1, 2.0)
try:
    p = TypedPoint('a', 'b')
except TypeError as e:
    print(e)


# We can enumerate specific allowed classes (like isinstance()).

class IntFloatPoint(Struct):
    x = TypedField((int, float))
    y = TypedField((int, float))

p = IntFloatPoint(1, 2.0)
try:
    p = IntFloatPoint(1j, 2 + 3j)
except TypeError as e:
    print(e)


# We can take a sequence of values, all of which satisfy the
# type specification.

class Vector(Struct):
    vals = TypedField(Number, seq=True)

v = Vector([1, 2, 3, 4])
# The sequence is converted to a tuple to help ensure immutability.
print(v)
try:
    v = Vector(5)
except TypeError as e:
    print(e)
try:
    v = Vector([1, 'b', 3, 4])
except TypeError as e:
    print(e)
# Construction from non-sequence iterables like generators is disallowed.
try:
    v = Vector((x for x in range(1, 5)))
except TypeError as e:
    print(e)


# Sequences may be checked for uniqueness.
# (This is implemented naively in O(n^2) time.)

class Ids(Struct):
    vals = TypedField(int, seq=True, unique=True)

try:
    ids = Ids([1, 2, 3, 2])
except TypeError as e:
    print(e)


# If None is passed as the first argument of TypedField,
# any type is admitted.

class Array(Struct):
    vals = TypedField(None, seq=True)

a = Array([1, 'b', False])
# It still must be a sequence.
try:
    a = Array(True)
except TypeError as e:
    print(e)


# Typed fields can be set to allow None.

class Person(Struct):
    name = Field
    salary = TypedField(int, or_none=True)

a = Person('Alice', 100000)
b = Person('Bob', None)

# This is different from adding NoneType to the sequence of
# allowed types, as that would mean the elements could be
# any type. Also note that or_none=True does not make passing
# in the field value to the constructor optional.


# The same Field instance can be used as a descriptor multiple
# times. (Each occurrence automatically gets a copy.) This can
# help shorten definitions.

myfield = TypedField((int, float), or_none=True)

class NullablePoint(Struct):
    x = myfield
    y = myfield
    z = myfield

p = NullablePoint(1, 2.0, None)


# Struct-typed fields can be coerced from tuple values.

class Line(Struct):
    a = TypedField(TypedPoint)
    b = TypedField(TypedPoint)

line1 = Line(TypedPoint(1, 2), TypedPoint(3, 4))
line2 = Line((1, 2), (3, 4))
assert line1 == line2
