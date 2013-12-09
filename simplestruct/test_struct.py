"""Unit tests for struct.py."""


import unittest

from simplestruct.struct import *


class StructCase(unittest.TestCase):
    
    def testField(self):
        # Since we're just testing Field and not MetaStruct,
        # we need to bypass some of the meta machinery and be
        # more verbose.
        barfield = Field(int, 'seq')
        barfield.name = 'bar'
        class Foo:
            bar = barfield
            def __init__(self, b):
                self._immutable = False
                self.bar = b
        
        # Instantiation.
        f = Foo([5])
        self.assertEquals(f.bar, [5])
        
        # Type checking.
        with self.assertRaises(TypeError):
            f.bar = 'b'
        
        # Immutability.
        f._immutable = True
        with self.assertRaises(AttributeError):
            f.bar = [6]
    
    def testStruct(self):
        # Basic functionality.
        class Foo(Struct):
            bar = Field(int)
        f = Foo(5)
        self.assertEqual(f.bar, 5)
        
        # Mutability.
        class Foo(Struct):
            _immutable = False
            bar = Field(int)
        f = Foo(5)
        f.bar = 6
        
        # Immutability.
        class Foo(Struct):
            bar = Field(int)
            def __init__(self, *_):
                self.bar += 1
        f = Foo(5)
        self.assertEqual(f.bar, 6)
        with self.assertRaises(AttributeError):
            f.bar = 7
        
        # Pretty-printing.
        self.assertEqual(str(f), 'Foo(bar=6)')
        
        # Derived data.
        class Foo(Struct):
            bar = Field(int)
            baz = Field(int, '!')
            def __init__(self, bar):
                self.baz = bar + 1
        f = Foo(5)
        self.assertEqual(f.baz, 6)
        
        # Equality and hashing.
        class Foo(Struct):
            bar = Field(int)
        f1 = Foo(5)
        f2 = Foo(5)
        f3 = Foo(6)
        self.assertEqual(f1, f2)
        self.assertNotEqual(f1, f3)
        self.assertEqual(hash(f1), hash(f2))
        # hash(f1) == hash(f3) is unlikely but valid.


if __name__ == '__main__':
    unittest.main()
