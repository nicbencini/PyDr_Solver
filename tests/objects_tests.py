import time
import numpy as np
import os
import sys
import unittest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/scpyce')


from objects import element
from objects import properties
from objects import load

class ElementTests(unittest.TestCase):

    def test_create_node(self):
        node1 = element.Node(0,0,0)
    
    def test_create_bar(self):

        node1 = element.Node(0,0,0)
        node2 = element.Node(0,0,1)
        section = properties.Section.default()
        orientation_vector = np.array([1,0,0])

        bar = element.Bar(node1,node2,section,orientation_vector)

    
    def test_create_support(self):

        node1 = element.Node(0,0,0)
        support1 = element.Support.pin(node1)

    
    def test_create_load(self):

        node1 = element.Node(0,0,0)
        load1 = load.PointLoad(node1,0,0,10,0,0,0)

    def test_local_stiffness_matrix(self):

        node1 = element.Node(0.5,0.5,1)
        node2 = element.Node(1,0,0)
        section = properties.Section.default()
        orientation_vector = np.array([0,0,1])

        bar1 = element.Bar(node1,node2,section,orientation_vector)

        Kl = bar1.local_stiffness_matrix()
        TM = bar1.transformation_matrix()
        

        control_KL = [[2109010668.5363169,0,0,0,0,0,-2109010668.5363169,0,0,0,0,0],
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
        
        control_TM= [[0.4082483,-0.4082483,-0.8164966,0,0,0.0000000,0,0,0,0,0,0.0000000],
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

        control_Kg = [[5.03359691e+08,-4.03114813e+08,-6.01268082e+08,5.12403860e+07,1.01362825e+08,-2.50612195e+07,-5.03359691e+08,4.03114813e+08,6.01268082e+08,5.12403860e+07,1.01362825e+08,-2.50612195e+07],
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



        Kl = np.round(Kl,7)
        TM = np.round(TM,7)

        self.assertSequenceEqual(Kl[0].tolist(),control_KL[0])
        self.assertSequenceEqual(Kl[1].tolist(),control_KL[1])
        self.assertSequenceEqual(Kl[2].tolist(),control_KL[2])
        self.assertSequenceEqual(Kl[3].tolist(),control_KL[3])
        self.assertSequenceEqual(Kl[4].tolist(),control_KL[4])
        self.assertSequenceEqual(Kl[5].tolist(),control_KL[5])
        self.assertSequenceEqual(Kl[6].tolist(),control_KL[6])
        self.assertSequenceEqual(Kl[7].tolist(),control_KL[7])
        self.assertSequenceEqual(Kl[8].tolist(),control_KL[8])
        self.assertSequenceEqual(Kl[9].tolist(),control_KL[9])
        self.assertSequenceEqual(Kl[10].tolist(),control_KL[10])
        self.assertSequenceEqual(Kl[11].tolist(),control_KL[11])

        self.assertSequenceEqual(TM[0].tolist(),control_TM[0])
        self.assertSequenceEqual(TM[1].tolist(),control_TM[1])
        self.assertSequenceEqual(TM[2].tolist(),control_TM[2])
        self.assertSequenceEqual(TM[3].tolist(),control_TM[3])
        self.assertSequenceEqual(TM[4].tolist(),control_TM[4])
        self.assertSequenceEqual(TM[5].tolist(),control_TM[5])
        self.assertSequenceEqual(TM[6].tolist(),control_TM[6])
        self.assertSequenceEqual(TM[7].tolist(),control_TM[7])
        self.assertSequenceEqual(TM[8].tolist(),control_TM[8])
        self.assertSequenceEqual(TM[9].tolist(),control_TM[9])
        self.assertSequenceEqual(TM[10].tolist(),control_TM[10])
        self.assertSequenceEqual(TM[11].tolist(),control_TM[11])

 


if __name__ == '__main__':
    unittest.main()
