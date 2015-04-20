#encoding:utf-8
'''
Created on Apr 1, 2015

@author: root

refernce:http://www.ibm.com/developerworks/cn/linux/l-pyunit/

most use method in the pyuint unittest:

assertEqual(a, b)     a == b      
assertNotEqual(a, b)     a != b      
assertTrue(x)     bool(x) is True      
assertFalse(x)     bool(x) is False      
assertIs(a, b)     a is b     2.7
assertIsNot(a, b)     a is not b     2.7
assertIsNone(x)     x is None     2.7
assertIsNotNone(x)     x is not None     2.7
assertIn(a, b)     a in b     2.7
assertNotIn(a, b)     a not in b     2.7
assertIsInstance(a, b)     isinstance(a, b)     2.7
assertNotIsInstance(a, b)     not isinstance(a, b)     2.7
assertAlmostEqual(a, b)     round(a-b, 7) == 0      
assertNotAlmostEqual(a, b)     round(a-b, 7) != 0      
assertGreater(a, b)     a > b     2.7
assertGreaterEqual(a, b)     a >= b     2.7
assertLess(a, b)     a < b     2.7
assertLessEqual(a, b)     a <= b     2.7
assertRegexpMatches(s, re)     regex.search(s)     2.7
assertNotRegexpMatches(s, re)     not regex.search(s)     2.7
assertItemsEqual(a, b)     sorted(a) == sorted(b) and works with unhashable objs     2.7
assertDictContainsSubset(a, b)     all the key/value pairs in a exist in b     2.7
assertMultiLineEqual(a, b)     strings     2.7
assertSequenceEqual(a, b)     sequences     2.7
assertListEqual(a, b)     lists     2.7
assertTupleEqual(a, b)     tuples     2.7
assertSetEqual(a, b)     sets or frozensets     2.7
assertDictEqual(a, b)     dicts     2.7
assertMultiLineEqual(a, b)     strings     2.7
assertSequenceEqual(a, b)     sequences     2.7
assertListEqual(a, b)     lists     2.7
assertTupleEqual(a, b)     tuples     2.7
assertSetEqual(a, b)     sets or frozensets     2.7
assertDictEqual(a, b)     dicts     2.7 
'''
import unittest
from widget import *
class WidgetTestCase(unittest.TestCase):
    def tearDown(self):
        pass
    def setUp(self):
        '''
        self.widget will generate the Widget instance to be the WidgetTestCase part
        self present the addresss of instance
        '''
        self.widget = Widget()
    def testDefaultSize(self):
        self.assertEqual(self.widget.getSize(), (40, 40))
    def testRise(self):
        self.widget.resize(10,10)
        self.assertEqual(self.widget.getSize(), (10, 10))
    def test_python2_7(self):
        self.assertGreater(10,6)
#     def runTest(self):
#         widget = Widget()
#         self.assertEqual(widget.getSize(), (40, 40))
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('testDefaultSize'))
    return suite

if __name__ == '__main__':
    '''
    two method:
    1.name the method start with the 'testXX',and use the unittest.main() to run  the test
    2.use the unittest.TestSuite() ,and generate the unittest.TextTestRunner()
    '''
#     runner = unittest.TextTestRunner()
#     runner.run(suite())
    unittest.main()
    