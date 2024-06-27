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
from geometry import vector_3d

db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'db_1.db'

class SolverTests(unittest.TestCase):

    def test_build_global_stiffness_matrix(self):
        
        structural_model = database.Model(db_path)

        D = lind_solver.solve(structural_model)

        #print (D)

        structural_model.close_connection()  


if __name__ == '__main__':
    unittest.main()