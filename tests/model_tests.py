"""
Module Description
"""

import os
import unittest
import numpy as np

from context import database # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error

db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_1_model_test.db'

class DatabaseTests(unittest.TestCase):
    """
    Class Description
    """

    def test_build_database(self):
        """Description"""

        node1 = element.Node(0.5,0.5,1)
        node2 = element.Node(1,0,0)
        node3 = element.Node(0,0,0)
        node4 = element.Node(1,1,0)
        node5 = element.Node(0,1,0)

        section = properties.Section.default()
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

        structural_model = database.Model(db_path)
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

        structural_model.close_connection()


    def test_get_material(self):
        """Description"""

        structural_model = database.Model(db_path)

        material = structural_model.get_material('steel')

        structural_model.close_connection()

        self.assertEqual(material.name, 'steel')
        self.assertEqual(material.youngs_modulus, 210000.0)
        self.assertEqual(material.poissons_ratio, 0.3)
        self.assertEqual(material.shear_modulus, 76903.07)
        self.assertEqual(material.coeff_thermal_expansion, 1.17e-05)
        self.assertEqual(material.damping_ratio, 0.0)
        self.assertEqual(material.density, 76.9729)
        self.assertEqual(material.type, 'STEEL')
        self.assertEqual(material.region, 'UK')
        self.assertEqual(material.embodied_carbon, 12090.0)

    def test_get_section(self):
        """Description"""

        structural_model = database.Model(db_path)

        section = structural_model.get_section('UC305x305x97')

        self.assertEqual(section.name, 'UC305x305x97')
        self.assertEqual(section.material.name, 'steel')
        self.assertEqual(section.area, 0.0123)
        self.assertEqual(section.izz, 0.0002225)
        self.assertEqual(section.iyy, 7.308e-05)

        structural_model.close_connection()

    def test_get_node(self):
        """Description"""

        structural_model = database.Model(db_path)

        node = structural_model.get_node(3)

        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 1)
        self.assertEqual(node.z, 0)

        structural_model.close_connection()

    def test_get_bar(self):
        """Description"""

        structural_model = database.Model(db_path)

        test_bar = structural_model.get_bar('5b324ddf-4c1e-42a1-b02a-4d9309498fb3')

        structural_model.close_connection()


if __name__ == '__main__':
    unittest.main()
