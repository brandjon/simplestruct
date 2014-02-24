"""Unit tests for util.py."""


import unittest

from simplestruct.util import *


class UtilCase(unittest.TestCase):
    
    def testTrim(self):
        text1 = trim('''
            for x in foo:
                print(x)
            ''')
        exp_text1 = 'for x in foo:\n    print(x)'
        
        self.assertEqual(text1, exp_text1)
        
        text2 = trim('')
        exp_text2 = ''
        
        self.assertEqual(text2, exp_text2)
    
    def testFrozendict(self):
        d = frozendict({1:2, 3:4})
        with self.assertRaises(TypeError):
            d[3] = 5
        hash(d)
    
    def testFreeze(self):
        val = make_frozen([{1: 2}, {3}])
        exp_val = (frozendict({1: 2}), frozenset({3}))
        self.assertEqual(val, exp_val)


if __name__ == '__main__':
    unittest.main()
