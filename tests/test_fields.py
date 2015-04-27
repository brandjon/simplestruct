"""Unit tests for fields.py."""


import unittest

from simplestruct.struct import *
from simplestruct.fields import *


class FieldsCase(unittest.TestCase):
    
    def test_TypedField(self):
        # Non-sequence case.
        class Foo(Struct):
            bar = TypedField(int)
        f = Foo(1)
        with self.assertRaises(TypeError):
            Foo('a')
        with self.assertRaises(TypeError):
            Foo(None)
        
        # Sequence case.
        class Foo(Struct):
            bar = TypedField(int, seq=True)
        f = Foo([1, 2])
        self.assertEqual(f.bar, ((1, 2)))
        with self.assertRaises(TypeError):
            Foo([1, 'a'])
        
        # Sequence without duplicates.
        class Foo(Struct):
            bar = TypedField(int, seq=True, unique=True)
        Foo([1, 2])
        with self.assertRaises(TypeError):
            Foo([1, 2, 1])
        
        # Optional case.
        class Foo(Struct):
            _immutable = False
            bar = TypedField(int, or_none=True)
        f1 = Foo(None)

    def test_nestedstructs(self):
        class Bar(Struct):
            a = Field
        class Foo(Struct):
            b = Field
            c = TypedField(Bar)
        f = Foo(1, (2,))
        self.assertEqual(f.c.a, 2)
        self.assertEqual(f.b, 1)
        with self.assertRaises(TypeError):
            f = Foo(1, 2)
        with self.assertRaises(TypeError):
            f = Foo(1, (2, 3))

if __name__ == '__main__':
    unittest.main()
