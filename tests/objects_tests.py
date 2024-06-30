"""
Module Description
"""

import unittest
import numpy as np

from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error

class ElementTests(unittest.TestCase):
    """
    Class Description
    """

    def test_create_node(self):
        """Description"""
        node1 = element.Node(0,0,0)

    def test_create_bar(self):
        """Description"""

        node1 = element.Node(0,0,0)
        node2 = element.Node(0,0,1)
        section = properties.Section.default()
        orientation_vector = np.array([1,0,0])

        bar = element.Bar(node1,node2,section,orientation_vector)


    def test_create_support(self):
        """Description"""

        node1 = element.Node(0,0,0)
        support1 = element.Support.pin(node1)


    def test_create_load(self):
        """Description"""

        node1 = element.Node(0,0,0)
        load1 = load.PointLoad(node1,0,0,10,0,0,0)

    def test_local_stiffness_matrix(self):
        """Description"""

        node1 = element.Node(0.5,0.5,1)
        node2 = element.Node(1,0,0)
        section = properties.Section.default()
        orientation_vector = np.array([0,0,1])

        bar1 = element.Bar(node1,node2,section,orientation_vector)

        kl = bar1.local_stiffness_matrix()
        tm = bar1.transformation_matrix()

        control_kl = [[2109010668.5363169,0,0,0,0,0,-2109010668.5363169,0,0,0,0,0],
                      [0,305206421.9507840,0,0,0,-186900000.0000000,0,-305206421.9507840,0,0,0,-186900000.0000000],
                      [0,0,100244877.8254530,0,61387200.0000000,0,0,0,-100244877.8254530,0,61387200.0000000,0],
                      [0,0,0,18559791.4811208,0,0,0,0,0,-18559791.4811208,0,0],
                      [0,0,61387200.0000000,0,50122438.9127265,0,0,0,-61387200.0000000,0,25061219.4563633,0],
                      [0,-186900000.0000000,0,0,0,152603210.9753920,0,186900000.0000000,0,0,0,76301605.4876960],
                      [-2109010668.5363169,0,0,0,0,0,2109010668.5363169,0,0,0,0,0],
                      [0,-305206421.9507840,0,0,0,186900000.0000000,0,305206421.9507840,0,0,0,186900000.0000000],
                      [0,0,-100244877.8254530,0,-61387200.0000000,0,0,0,100244877.8254530,0,-61387200.0000000,0],
                      [0,0,0,-18559791.4811208,0,0,0,0,0,18559791.4811208,0,0],
                      [0,0,61387200.0000000,0,25061219.4563633,0,0,0,-61387200.0000000,0,50122438.9127265,0],
                      [0,-186900000.0000000,0,0,0,76301605.4876960,0,186900000.0000000,0,0,0,152603210.9753920]]

        control_tm= [[0.4082483,-0.4082483,-0.8164966,0,0,0.0000000,0,0,0,0,0,0.0000000],
                    [0.5773503,-0.5773503,0.5773503,0,0,0.0000000,0,0,0,0,0,0.0000000],
                    [-0.7071068,-0.7071068,0,0,0,0.0000000,0,0,0,0,0,0.0000000],
                    [0,0,0,0.4082483,-0.4082483,-0.8164966,0,0,0,0,0,0.0000000],
                    [0,0,0,0.5773503,-0.5773503,0.5773503,0,0,0,0,0,0.0000000],
                    [0,0,0.0000000,-0.7071068,-0.7071068,0.0000000,0,0,0,0,0,0.0000000],
                    [0,0,0,0,0,0.0000000,0.4082483,-0.4082483,-0.8164966,0,0,0.0000000],
                    [0,0,0,0,0,0.0000000,0.5773503,-0.5773503,0.5773503,0,0,0.0000000],
                    [0,0,0,0,0,0.0000000,-0.7071068,-0.7071068,0,0,0,0.0000000],
                    [0,0,0,0,0,0.0000000,0,0,0,0.4082483,-0.4082483,-0.8164966],
                    [0,0,0,0,0,0.0000000,0,0,0,0.5773503,-0.5773503,0.5773503],
                    [0,0,0,0,0,0.0000000,0,0,0.0000000,-0.7071068,-0.7071068,0.0000000]]

        control_kg = [[5.03359691e+08,-4.03114813e+08,-6.01268082e+08,5.12403860e+07,1.01362825e+08,-2.50612195e+07,-5.03359691e+08,4.03114813e+08,6.01268082e+08,5.12403860e+07,1.01362825e+08,-2.50612195e+07],
                      [-4.03114813e+08,5.03359691e+08,6.01268082e+08,-1.01362825e+08,-5.12403860e+07,-2.50612195e+07,4.03114813e+08,-5.03359691e+08,-6.01268082e+08,-1.01362825e+08,-5.12403860e+07,-2.50612195e+07],
                      [-6.01268082e+08,6.01268082e+08,1.50774259e+09,7.63016055e+07,7.63016055e+07,0.00000000e+00,6.01268082e+08,-6.01268082e+08,-1.50774259e+09,7.63016055e+07,7.63016055e+07,0.00000000e+00],
                      [5.12403860e+07,-1.01362825e+08,7.63016055e+07,9.61023837e+07,5.65008273e+07,1.05208825e+07,-5.12403860e+07,1.01362825e+08,-7.63016055e+07,4.34112440e+07,3.28903615e+07,1.45403370e+07],
                      [1.01362825e+08,-5.12403860e+07,7.63016055e+07,5.65008273e+07,9.61023837e+07,-1.05208825e+07,-1.01362825e+08,5.12403860e+07,-7.63016055e+07,3.28903615e+07,4.34112440e+07,-1.45403370e+07],
                      [-2.50612195e+07,-2.50612195e+07,0.00000000e+00,1.05208825e+07,-1.05208825e+07,2.90806740e+07,2.50612195e+07,2.50612195e+07,0.00000000e+00,1.45403370e+07,-1.45403370e+07,-4.01945450e+06],
                      [-5.03359691e+08,4.03114813e+08,6.01268082e+08,-5.12403860e+07,-1.01362825e+08,2.50612195e+07,5.03359691e+08,-4.03114813e+08,-6.01268082e+08,-5.12403860e+07,-1.01362825e+08,2.50612195e+07],
                      [4.03114813e+08,-5.03359691e+08,-6.01268082e+08,1.01362825e+08,5.12403860e+07,2.50612195e+07,-4.03114813e+08,5.03359691e+08,6.01268082e+08,1.01362825e+08,5.12403860e+07,2.50612195e+07],
                      [6.01268082e+08,-6.01268082e+08,-1.50774259e+09,-7.63016055e+07,-7.63016055e+07,0.00000000e+00,-6.01268082e+08,6.01268082e+08,1.50774259e+09,-7.63016055e+07,-7.63016055e+07,0.00000000e+00],
                      [5.12403860e+07,-1.01362825e+08,7.63016055e+07,4.34112440e+07,3.28903615e+07,1.45403370e+07,-5.12403860e+07,1.01362825e+08,-7.63016055e+07,9.61023837e+07,5.65008273e+07,1.05208825e+07],
                      [1.01362825e+08,-5.12403860e+07,7.63016055e+07,3.28903615e+07,4.34112440e+07,-1.45403370e+07,-1.01362825e+08,5.12403860e+07,-7.63016055e+07,5.65008273e+07,9.61023837e+07,-1.05208825e+07],
                      [-2.50612195e+07,-2.50612195e+07,0.00000000e+00,1.45403370e+07,-1.45403370e+07,-4.01945450e+06,2.50612195e+07,2.50612195e+07,0.00000000e+00,1.05208825e+07,-1.05208825e+07,2.90806740e+07]
                      ]



        kl = np.round(kl,7)
        tm = np.round(tm,7)

        self.assertSequenceEqual(kl[0].tolist(),control_kl[0])
        self.assertSequenceEqual(kl[1].tolist(),control_kl[1])
        self.assertSequenceEqual(kl[2].tolist(),control_kl[2])
        self.assertSequenceEqual(kl[3].tolist(),control_kl[3])
        self.assertSequenceEqual(kl[4].tolist(),control_kl[4])
        self.assertSequenceEqual(kl[5].tolist(),control_kl[5])
        self.assertSequenceEqual(kl[6].tolist(),control_kl[6])
        self.assertSequenceEqual(kl[7].tolist(),control_kl[7])
        self.assertSequenceEqual(kl[8].tolist(),control_kl[8])
        self.assertSequenceEqual(kl[9].tolist(),control_kl[9])
        self.assertSequenceEqual(kl[10].tolist(),control_kl[10])
        self.assertSequenceEqual(kl[11].tolist(),control_kl[11])

        self.assertSequenceEqual(tm[0].tolist(),control_tm[0])
        self.assertSequenceEqual(tm[1].tolist(),control_tm[1])
        self.assertSequenceEqual(tm[2].tolist(),control_tm[2])
        self.assertSequenceEqual(tm[3].tolist(),control_tm[3])
        self.assertSequenceEqual(tm[4].tolist(),control_tm[4])
        self.assertSequenceEqual(tm[5].tolist(),control_tm[5])
        self.assertSequenceEqual(tm[6].tolist(),control_tm[6])
        self.assertSequenceEqual(tm[7].tolist(),control_tm[7])
        self.assertSequenceEqual(tm[8].tolist(),control_tm[8])
        self.assertSequenceEqual(tm[9].tolist(),control_tm[9])
        self.assertSequenceEqual(tm[10].tolist(),control_tm[10])
        self.assertSequenceEqual(tm[11].tolist(),control_tm[11])

if __name__ == '__main__':
    unittest.main()
