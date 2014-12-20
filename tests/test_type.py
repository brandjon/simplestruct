"""Unit tests for type.py."""


import unittest

from simplestruct.type import *


class ChecktypeCase(unittest.TestCase):
    
    def setUp(self):
        self.checker = TypeChecker()
    
    def test_strs(self):
        c = self.checker
        self.assertEqual(c.str_valtype(None), 'None')
        self.assertEqual(c.str_valtype(5), 'int')
        self.assertEqual(c.str_kind(()), 'Nothing')
        self.assertEqual(c.str_kind((int,)), 'int')
        self.assertEqual(c.str_kind((int, str)), 'int or str')
        self.assertEqual(c.str_kind((int, str, bool)),
                         'one of {int, str, bool}')
        
    def test_normalize(self):
        c = self.checker
        self.assertEqual(c.normalize_kind((int,)), (int,))
        self.assertEqual(c.normalize_kind([int,]), (int,))
        self.assertEqual(c.normalize_kind(int), (int,))
        self.assertEqual(c.normalize_kind(None), (object,))
    
    def test_checktype(self):
        c = self.checker
        
        c.checktype('a', (str,))
        c.checktype(True, (int,))    # This is correct, bool subtypes int
        c.checktype(5, (str, int))
        
        with self.assertRaisesRegex(
                TypeError, 'Expected int; got None'):
            c.checktype(None, (int,))
        with self.assertRaisesRegex(
                TypeError, 'Expected str or int; got None'):
            c.checktype(None, (str, int))
    
    def test_checktype_seq(self):
        c = self.checker
        
        c.checktype_seq([], (str,))
        c.checktype_seq([3, True], (int,))
        with self.assertRaisesRegex(
                TypeError, 'Expected sequence of bool; got sequence with '
                           'int at position 0'):
            c.checktype_seq([3, True], (bool,))
        with self.assertRaisesRegex(
                TypeError, 'Expected sequence of bool; '
                           'got bool instead of sequence'):
            c.checktype_seq(True, (bool,))
        with self.assertRaisesRegex(
                TypeError, 'Expected sequence of str; '
                           'got single str'):
            c.checktype_seq('abc', (str,))
        with self.assertRaisesRegex(
                TypeError, 'Expected sequence of int; '
                           'got generator instead of sequence'):
            c.checktype_seq((i for i in range(3)), (int,))
        
        c.checktype_seq([5, 3, 5, 8], (int,))
        with self.assertRaisesRegex(
                TypeError, 'Duplicate element 5 at position 2'):
            c.checktype_seq([5, 3, 5, 8], (int,), nodups=True)


if __name__ == '__main__':
    unittest.main()
