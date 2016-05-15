# Release notes

## 0.2.2 (2016-05-15)

- fields with default values are properly passed to __new__()/__init__()
- added support for coercion of tuples for Struct-typed fields
- added support for `__getitem__` and `__setitem__`
- testing a Struct for equality with itself succeeds quickly

## 0.2.1 (2014-12-20)

- changed type checking keyword argument names: `opt` -> `or_none`
  and `nodups` -> `unique`
- improved error messages for constructing Structs
- significant updates to readme and examples
- using `opt=True` on `TypedField` no longer implies that `None` is
  the default value
- made mixin version of `checktype()` and `checktype_seq()`
- added `check()` and `normalize()` hooks to `TypedField`
- accessing fields descriptors from classes is now permissible
- added support for default values in general, and optional values
  for type-checked fields
- fixed `__repr__()` on recursive Structs

## 0.2.0 (2014-12-15)

- initial release
