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

    def test_NestedStruct(self):
        class Foo(Struct):
            a = Field
            class Bar(Struct):
                a = Field
            b = TypedField(Bar)
        t = (1, (2,))
        f = Foo(*t)
        self.assertEqual(f.b.a, 2)
        self.assertEqual(f.a, 1)
        with self.assertRaises(TypeError):
            f = Foo(*(1, 2))
        with self.assertRaises(TypeError):
            f = Foo(*(1, (2, 3)))

if __name__ == '__main__':
    unittest.main()
