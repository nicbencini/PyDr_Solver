import time
import numpy as np
import os
import sys
import unittest

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/scpyce')

from model import database
from engine import lind_solver
from objects import element
from objects import property
from objects import load

db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_2_lind_solver_test.db'

class LindSolverTests(unittest.TestCase):

    def test_build_database(self):
        

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


    def test_build_global_stiffness_matrix(self):
        
        structural_model = database.Model(db_path)

        D = lind_solver.solve(structural_model)

        #print (D)

        structural_model.close_connection()  


if __name__ == '__main__':
    unittest.main()