"""Unit tests for struct.py."""


import unittest
from collections import OrderedDict

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
        self.assertEqual(f.bar, (5,))
        
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
        
        # Construction by keyword.
        class Foo(Struct):
            a = Field()
            b = Field()
            c = Field()
        f1 = Foo(1, b=2, **{'c': 3})
        f2 = Foo(1, 2, 3)
        self.assertEqual(f1, f2)
        
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
        
        # No hashing for mutable structs.
        class Foo(Struct):
            _immutable = False
            bar = Field(int)
        f = Foo(5)
        with self.assertRaises(TypeError):
            hash(f)
        
        # Or for structs that aren't yet constructed.
        class Foo(Struct):
            bar = Field(int)
            def __init__(self, bar):
                hash(self)
            hash(self)
        with self.assertRaises(TypeError):
            f = Foo(5)
    
    def testCustomEqHash(self):
        class CustomField(Field):
            def eq(self, val1, val2):
                return val1 * val2 > 0
            def hash(self, val):
                return int(val) * 2
        
        class FooA(Struct):
            bar = Field(float, 'seq')
        class FooB(Struct):
            bar = CustomField(float, 'seq')
        
        fa1 = FooA([5.0])
        fa2 = FooA([6.0])
        fb1 = FooB([5.0])
        fb2 = FooB([6.0])
        
        self.assertNotEqual(fa1, fa2)
        self.assertNotEqual(hash(fa1), 10)
        self.assertEqual(fb1, fb2)
        self.assertEqual(hash(fb1), 10)
    
    def testDict(self):
        class Foo(Struct):
            a = Field()
            b = Field()
            c = Field()
        f = Foo(1, 2, 3)
        d = f._asdict()
        exp_d = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(d, exp_d)
    
    def testReplace(self):
        class Foo(Struct):
            a = Field()
            b = Field()
            c = Field()
        f1 = Foo(1, 2, 3)
        f2 = f1._replace(b=4)
        f3 = Foo(1, 4, 3)
        self.assertEqual(f2, f3)


if __name__ == '__main__':
    unittest.main()
