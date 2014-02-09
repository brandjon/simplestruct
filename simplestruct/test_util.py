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


if __name__ == '__main__':
    unittest.main()
