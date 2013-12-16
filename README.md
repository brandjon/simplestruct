SimpleStruct
============

*(Requires Python 3)*

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


### To use ###

For the simplest case, just use

    from simplestruct import Struct, Field
    
    class Point(Struct):
        x = Field(int)
        y = Field(int)

to get a simple Point class. No need to define `__init__()`, `__str__()`,
`__eq__()`, `__hash__()`, etc. See the examples/ directory for more.


### Comparison to namedtuple ###

The standard library's [namedtuple](http://docs.python.org/3/library/collections#collections.namedtuple)
feature can generate classes similar to what this library produces.
Specifically, namedtuple classes automatically get constructors, pretty-
printing, equality, and hashing, as well as sequential access (so you can use
decomposing assignment such as `x, y = mypoint`). They do *not* support type
checks and mutability, nor can you define auxiliary attributes on the object
since it is constructed all-at-once.

Namedtuples are implemented by specializing and then `eval()`ing a source code
template that describes the desired class. In contrast, SimpleStruct uses
inheritance and metaclasses to implement all struct's behavior in a generic
way. There is a performance penalty to this, since each operation results in
more function calls. An application that requires top performance out of each
struct operation should go with namedtuple if possible, especially because
much of its functionality is provided by the built-in Python tuple type.


### TODO ###

Features TODO:
- allow structs to be instantiated with keyword arguments
- add support for `__slots__`
- support iteration of fields (like namedtuple)
- make exceptions appear to be raised from the stack frame of user code
  where the type error occurred, rather than inside this library (with
  a flag to disable, for debugging)
- picklability
- possibly make it so the same Field object can be used to declare multiple
  structs, and the metaclass replaces this Field object with a copy so they
  can have different "name" attributes. This would allow defining a reusable
  kind of field without repeating kind/mods each time.

Packaging TODO:
- make usage examples
- fix up setup.py, make installable
