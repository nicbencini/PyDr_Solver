import time
import numpy as np
import os
import sys
import unittest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/scpyce')


class ElementTests(unittest.TestCase):

    def test_create_bar(self):

        from model import element
        from model import property

        node1 = element.Node(0,0,0)
        node2 = element.Node(0,0,1)
        section = property.Section.default()
        orientation_vector = np.array([1,0,0])

        bar = element.Bar(node1,node2,section,orientation_vector)


if __name__ == '__main__':
    unittest.main()
