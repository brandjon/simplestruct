# SimpleStruct #

*(Supports Python 3.3 and up)*

This small library makes it easier to create "struct" classes in Python
without writing boilerplate code. Structs are similar to the standard
library's [`collections.namedtuple`][1] but are more flexible, relying on an
inheritance-based approach instead of `eval()`ing a code template. If
you like using `namedtuple` classes but wish they were more composable
and extensible, this project is for you.

## Example ##

Writing struct classes by hand is tedious and error prone. Consider a
simple point class. The bare minimum we can write in Python is

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

We'll likely want to compare points for equality and pretty-print them
for debugging.

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        # Separate __str__() would be nice too
        return 'Point2D({!r}, {!r})'.format(self.x, self.y)
    def __eq__(self, other):
        # Should check other's type too
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        # Required because we're overriding __eq__().
        return hash(self.x) ^ hash(self.y)
```

Already the code is becoming pretty verbose for such a simple concept.
Worse, it violates the [DRY principle](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
in that the `x` and `y` fields appear many times. This isn't very
robust. If we decide to turn this into a `Point3D` class, we'll have
to upgrade each method to accommodate a new z coordinate. We could be
in for an infuriating bug if we forget to update `__eq__()` or
`__hash__()`. Adding more utilities like a copy/replace method will
exacerbate the situation.

Then there's the added code for consistency checking. Maybe you're the
sort of heathen who prefers dynamic type checking over blindly trusting
Mama Ducktype. Or maybe you want to disallow overwriting `x` and `y` so
as to avoid changing its hash value. Either way you'd need to use
descriptors or properties to intercept writes.

SimpleStruct provides a simple alternative. Here is a `Point2D` class
that provides everything described above.

```python
from numbers import Number      # standard library abstract base class
from simplestruct import Struct, Field, TypedField

class Point2D(Struct):
    # Note that field declaration order matters.
    x = TypedField(Number)
    y = TypedField(Number)
```

Of course, customizations are possible. Type checking is by no means
required, objects may be mutable so long as they are not hashed,
and you can add your own non-Field attributes and properties.

```python
class Point2D(Struct):
    _immutable = False
    x = Field
    y = Field
    
    # magnitude won't be considered when hashing or testing equality
    @property
    def magnitude(self):
        return (self.x**2 + self.y**2) ** .5
```

For more usage examples, see the sample files:

File | Purpose
---|---
[point.py](examples/point.py) | introduction, basic use
[typed.py](examples/typed.py) | type-checked fields
[vector.py](examples/vector.py) | advanced features
[abstract.py](examples/abstract.py) | mixing structs and metaclasses

## Comparison and feature matrix ##

The most important problems mentioned above are solved by using
`namedtuple`, but this approach begins to break down when you
start to customize classes. To add a property to a `namedtuple`,
you must define a subclass:

```python
BasePerson = namedtuple('BasePerson', 'fname lname age')
class Person(BasePerson):
    @property
    def full_name(self):
        return self.fname + ' ' + self.lname
```

If on the other hand you want to extend an existing `namedtuple` with
new fields, it's a bit harder. You need to regenerate (not inherit)
the boilerplate methods so they recognize the new fields. This can be
done using multiple inheritance:

```python
BaseEmployee = namedtuple('BaseEmployee', BasePerson._fields + ('salary',))
class Employee(BaseEmployee, Person):
    pass
```

Implementation wise, `namedtuple` works by dynamically evaluating
a templated class definition based on the built-in `tuple` type.
This gives it a speed advantage, but is also the main reason why
it is less extensible (and unable to handle mutable values).

In contrast, SimpleStruct is based on metaclasses, descriptors, and
dynamic dispatch. The below matrix summarizes the feature comparison.

Feature | Avoids boilerplate for | Supported by `namedtuple`?
---|:---:|:---:
easy construction | `__init__()` | ✓
extra attributes on self | | subclasses only
pretty printing | `__str()__`, `__repr()__` | ✓
structural equality | `__eq__()` | ✓
easy inheritance | | ✗
optional mutability | | ✗
hashing (if immutable) | `__hash__()` | ✓
pickling / deep-copying |  | ✓
tuple decomposition | `__len__`, `__iter__` | ✓
indexing | `__getitem__`, `__setitem__` | `__getitem__` only
optional type checking | `__init__()`, `@property` | ✗
`_asdict()` / `_replace()` | | ✓

[MacroPy][2]'s "case classes" provide similar functionality, but are
implemented in a very different way. Instead of metaclass hacking
or source code templating, MacroPy relies on syntactic transformation
of the module's AST. This allows for a syntax that's very different
from what we've seen above. So different, in fact, that we might view
MacroPy as an extension to the Python language rather than as just
a library. Case classes are subject to limitations on
inheritance and class members.

## Installation ##

As with most Python packages, SimpleStruct is available on PyPI:

```
python -m pip install simplestruct
```

Or grab a development version if you're so inclined:

```
python -m pip install https://github.com/brandjon/simplestruct/tree/tarball/develop
```

Python 3.3 and 3.4 are supported. There are no additional dependencies.

## Developers ##

Tests can be run with `python setup.py test`, or alternatively by
installing [Tox](http://testrun.org/tox/latest/) and running 
`python -m tox` in the project root. Tox has the advantage of automatically
testing under both Python 3.3 and 3.4. Building a source distribution
(`python setup.py sdist`) requires the setuptools extension package
[setuptools-git](https://github.com/wichert/setuptools-git).

## References ##

[1]: https://docs.python.org/3/library/collections.html#collections.namedtuple
[[1]] The standard library's `namedtuple` feature

[2]: https://github.com/lihaoyi/macropy#case-classes
[[2]] Li Haoyi's case classes (part of MacroPy)

[3]: http://harts.net/reece/2013/06/02/using-namedtuples-with-method-and-instance-variable-inheritance/
[[3]] Reece Hart's blog post on inheriting from `namedtuple`
