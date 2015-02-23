# Bugs #
- equality testing of cyclic objects can cause infinite recursion.

```python
class A(Struct):
    x = Field()
a1 = A(None)
a2 = A(None)
a1.x = a2
a2.x = a1
a1 == a2
```
The proper behavior in this case should probably be to allow `a1 == a2`
to return `False` for simplicity, even though `a1` and `a2` are actually
isomorphic.

# Wishlist #
- add support for `__slots__`
- make exceptions appear to be raised from the stack frame of user code
  where the type error occurred, rather than inside this library (with
  a flag to disable, for debugging)
