import time
import numpy as np
import os
import sys
import unittest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/scpyce')


class VectorTests(unittest.TestCase):

    def test_vector_magnituce(self):

        from util import vector_math

        vector = (11,23,2)

        magnitude = vector_math.Vector.magnitude(vector)

        self.assertEqual(magnitude,25.573423705088842)

    def test_vector_unit(self):

        from util import vector_math

        vector = (11,23,2)

        unit_vector = vector_math.Vector.unit(vector)
        control_vector = np.array([0.4301340378531763,0.8993711700566414,0.07820618870057751])

        self.assertSequenceEqual(unit_vector.tolist(),control_vector.tolist())

    def test_vector_length(self):

        from util import vector_math

        vector_1 = (0,0,0)
        vector_2 = (11,23,2)

        length = vector_math.Vector.length(vector_1, vector_2)
        control_length = 25.573423705088842

        self.assertEqual(length, control_length)

    def test_vector_gram_schmit(self):

        from util import vector_math

        vector_1 = (11,23,2)
        vector_2 = (2,5,6)

        new_vector = vector_math.Vector.gram_schmit(vector_1 , vector_2)
        control_vector = np.array([-1637,-3422,-292])

        self.assertSequenceEqual(new_vector.tolist(),control_vector.tolist())


    def test_local_plane(self):

        from util import vector_math

        point_1 = np.array([0.5,0.5,1])
        point_2 = np.array([1,0,0])
        vector = np.array([0,0,1])

        new_plane = vector_math.Plane.plane_from_3pt(point_1, point_2, vector)

        new_plane_origin = new_plane[0]
        new_plane_x_vec = new_plane[1]
        new_plane_y_vec = new_plane[2]
        new_plane_z_vec = new_plane[3]

        control_plane_origin = np.array([0.5, 0.5, 1])
        control_plane_x_vec = np.array([0.5773502691896258, -0.5773502691896258, 0.5773502691896254])
        control_plane_y_vec = np.array([-0.7071067811865476, -0.7071067811865476, 0])
        control_plane_z_vec = np.array([0.4082482904638631, -0.4082482904638631, -0.8164965809277261])

        self.assertSequenceEqual(new_plane_origin.tolist(),control_plane_origin.tolist())
        self.assertSequenceEqual(new_plane_x_vec.tolist(),control_plane_x_vec.tolist())
        self.assertSequenceEqual(new_plane_y_vec.tolist(),control_plane_y_vec.tolist())
        self.assertSequenceEqual(new_plane_z_vec.tolist(),control_plane_z_vec.tolist())

class ElementTests(unittest.TestCase):

    def test_create_bar(self):

        from objects import element
        from objects import property

        node1 = element.Node(0,0,0)
        node2 = element.Node(0,0,1)
        section = property.Section.default()
        orientation_vector = np.array([1,0,0])

        bar = element.Bar(node1,node2,section,orientation_vector)


class SolverTests(unittest.TestCase):

    def test_local_stiffness_matrix(self):

        from data import database
        from objects import element
        from objects import property
        from objects import load
        from engine import stiffness_matrix
        from util import vector_math

        node1 = element.Node(0.5,0.5,1)
        node2 = element.Node(1,0,0)
        section = property.Section.default()
        material = section.material
        orientation_vector = np.array([0,0,1])

        length = vector_math.Vector.length(node1.to_array(),node2.to_array())

        print(length)

        local_plane = vector_math.Plane.plane_from_3pt(node1.to_array(),node2.to_array(), orientation_vector)

        bar1 = element.Bar(node1,node2,section,orientation_vector)

        Kl, Kg = stiffness_matrix.LocalStiffnessMatrix.build(section.area,
                                                             material.youngs_modulus,
                                                             section.izz,
                                                             section.iyy,
                                                             material.shear_modulus,
                                                             length,
                                                             local_plane,
                                                             bar1.release_a,
                                                             bar1.release_b
                                                             )
        
    

        control_KL = [[2.10901906e+09,0,0,0,0,0,-2.10901906e+09,0,0,0,0,0],
                      [0,3.05210064e+08,0,0,0,-1.86901487e+08,0,-3.05210064e+08,0,0,0 -1.86901487e+08],
                      [0,0,1.00246074e+08,0,6.13876883e+07,0,0,0,-1.00246074e+08,0,6.13876883e+07,0],
                      [0,0,0,1.85598653e+07,0,0,0,0,0,-1.85598653e+07,0,0],
                      [0,0,6.13876883e+07,0,5.01226383e+07,0,0,0,-6.13876883e+07,0,2.50613191e+07,0],
                      [0,-1.86901487e+08,0,0,0,1.52603818e+08,0,1.86901487e+08,0,0,0,7.63019090e+07],
                      [-2.10901906e+09,0,0,0,0,0,2.10901906e+09,0,0,0,0,0],
                      [0,-3.05210064e+08,0,0,0,1.86901487e+08,0,3.05210064e+08,0,0,0,1.86901487e+08],
                      [0,0,-1.00246074e+08,0,-6.13876883e+07,0,0,0,1.00246074e+08,0,-6.13876883e+07,0],
                      [0,0,0,-1.85598653e+07,0,0,0,0,0,1.85598653e+07,0,0],
                      [0,0,6.13876883e+07,0,2.50613191e+07,0,0,0,-6.13876883e+07,0,5.01226383e+07,0],
                      [0,-1.86901487e+08,0,0,0,7.63019090e+07,0,1.86901487e+08,0,0,0,1.52603818e+08]]
        
        self.assertSequenceEqual(Kl[0],control_KL[0])



    def test_pyramid(self):

        from data import database
        from objects import element
        from objects import property
        from objects import load
        from engine import stiffness_matrix

        node1 = element.Node(0.5,0.5,1)
        node2 = element.Node(1,0,0)
        node3 = element.Node(0,0,0)
        node4 = element.Node(1,1,0)
        node5 = element.Node(0,1,0)

        section = property.Section.default()
        orientation_vector = np.array([1,0,0])

        bar1 = element.Bar(node1,node2,section,orientation_vector)
        bar2 = element.Bar(node1,node3,section,orientation_vector)
        bar3 = element.Bar(node1,node4,section,orientation_vector)
        bar4 = element.Bar(node1,node5,section,orientation_vector)

        support1 = element.Support.pin(node2)
        support2 = element.Support.pin(node3)
        support3 = element.Support.pin(node4)
        support4 = element.Support.pin(node5)

        load1 = load.PointLoad(node1,0,0,10,0,0,0)

        structural_model = database.Model('/home/nicbencini/', 'test')
        structural_model.build_tables()


        structural_model.add_bar(bar1)
        structural_model.add_bar(bar2)
        structural_model.add_bar(bar3)
        structural_model.add_bar(bar4)

        structural_model.add_support(support1)
        structural_model.add_support(support2)
        structural_model.add_support(support3)
        structural_model.add_support(support4)

        structural_model.add_point_load(load1)

        sm = stiffness_matrix.GlobalStiffnessMatrix(structural_model)

        bar_cursor = structural_model.connection.cursor()

        structural_model.close_connection()


if __name__ == '__main__':
    unittest.main()