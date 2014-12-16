# SimpleStruct

*(Supports Python 3.3 and up)*

This is a small utility for making it easier to create "struct" classes
in Python without writing boilerplate code. Structs are similar to the
standard library's `collections.namedtuple` but are more flexible,
relying on an inheritance-based approach instead of `eval()`ing a code
template.

## Example

Writing struct classes by hand is tedious and error prone. Consider a
simple Point2D class. The bare minimum we can write is

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

but for it to be of any use, we'll need structural equality semantics
and perhaps some pretty printing for debugging.

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        print('Point2D({}, {})'.format(self.x, self.y))
    __str__ = __repr__
    def __eq__(self, other):
        # Nevermind type-checking and subtyping.
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
```

If you're the sort of heathen who likes to use dynamic type checks
in Python code, you'll want to add extra argument checking to the
constructor. And we'll probably want to disallow inadvertently
reassigning to x and y after construction, or else the hash value
could become inconsistent -- a big problem if the point is stored
in a hash-based collection.

Even if we do all that, the code isn't robust to change. If we decide
to make this a Point3D class, we'll have to update each method to
accommodate the new z coordinate. One oversight and we're in for a
potentially hard-to-find bug.

`namedtuple` takes care of many of these problems, but it's not
extensible. You can't easily derive a new class from a namedtuple
class without implementing much of this boilerplate. It also forces
immutability, which may be inappropriate for your use case.

SimpleStruct provides a simple alternative. For the above case,
we just write

    from simplestruct import Struct, Field
    
    class Point2D(Struct):
        x = Field
        y = Field

## Feature matrix

Feature | Avoids boilerplate for | Supported by `namedtuple`?
---|:---:|:---:
construction | `__init__()` | ✓
extra attributes on self | | ✗
pretty printing | `__str()__`, `__repr()__` | ✓
structural equality | `__eq__()` | ✓
inheritance | | ✗
optional mutability | | ✗
hashing (if immutable) | `__hash__()` | ✓
pickling / deep-copying |  | ✓
tuple decomposition | `__len__`, `__iter__` | ✓
optional type checking | | ✗

The `_asdict()` and `_replace()` methods from `namedtuple` are also
provided.

One advantage that `namedtuple` does have is speed. It is based on
the built-in Python tuple type, whereas SimpleStruct has the added
overhead of descriptor function calls.


## To use ###

See the `examples/` directory.


## Developers ##

Tests can be run with

```
python setup.py test
```
or alternatively by installing [Tox](http://testrun.org/tox/latest/) and
running 
```
python -m tox
```
in the project root. Tox has the advantage of automatically testing both
Python 3.3 and 3.4.

## TODO ###

Features TODO:
- add support for `__slots__`
- make exceptions appear to be raised from the stack frame of user code
  where the type error occurred, rather than inside this library (with
  a flag to disable, for debugging)
