SimpleStruct
============

(Requires Python 3.)

This is a small utility for making it easier to write simple struct
classes in Python, without having to write boilerplate code. Structs
are similar to the standard library's namedtuple, but support type
checking, mutability, and derived data (i.e. cached properties).

A struct is a class defining one or more named fields. The constructor
takes in the non-derived fields, in the order they were declared.
Structs can be compared for equality -- two instances of the same
struct compare equal if their fields are equal. The struct may be
declared as immutable or mutable; if immutable, modification is not
allowed after `__init__()` finishes, and the struct becomes hashable.
Structs are pretty-printed by `str()` and `repr()`.

Each field is declared with an optional type and modifiers. Types
are checked dynamically upon assignment (or reassignment). Modifiers
allow for lists of values, automatic type coersion, and for marking
fields as derived (computed by a user-defined `__init__()`).

This is a small toy project, so no backwards compatability guarantees
are made.


To use
------

For the simplest case, just use

    from simplestruct import Struct, Field
    
    class Point(Struct):
        x = Field(int)
        y = Field(int)

to get a simple Point class. No need to define `__init__()`, `__str__()`,
`__eq__()`, `__hash__()`, etc. See the examples/ directory for more.


Features TODO:
- allow structs to be instantiated with keyword arguments
- add support for `__slots__`
- support iteration of fields (like namedtuple)
- make exceptions appear to be raised from the stack frame of user code
  where the type error occurred, rather than inside this library (with
  a flag to disable, for debugging)
- picklability

Packaging TODO:
- make usage examples
- fix up setup.py, make installable
