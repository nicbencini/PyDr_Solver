import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import numpy as np
import sqlite3
from objects import element
from objects import property
from geometry import sc_vector


def solve(structural_stiffness_matrix, force_vector):
    
    displacement_vector = np.linalg.solve(structural_stiffness_matrix, force_vector)

    return displacement_vector


class StiffnessMatrix:

    """description of class"""

    def __init__(self, model):

        self.model = model
        self.bar_Kl_dict={}
        self.removed_indices_list = []

        # Initiate primary stiffness matrix

        node_cursor = model.connection.cursor()
        node_id_list = node_cursor.execute('SELECT _id FROM element_node').fetchall()
        node_cursor.close()

        self.ndof_primary =  len(node_id_list) * 6
        if((self.ndof_primary ** 2)*8 > 1e+9):
            raise RuntimeError('Stiffness matrix size exceeds 1GB. Reduce the number of elements in the model')
        else:
            self.primarty_stiffness_matrix = np.zeros((self.ndof_primary,self.ndof_primary),dtype=np.int8)

        # Initiate structural stiffness matrix
        self.ndof_structure = None
        self.structual_stiffness_matrix = None

        self.force_vector = None

    def build_primary(self):

        bar_cursor = self.model.connection.cursor()
        bar_cursor.execute('SELECT * FROM element_bar') 

        for bar in bar_cursor:

            bar_id = bar[0]
            node_i_index  = bar[1]
            node_j_index  = bar[2]

            bar_object = self.model.get_bar(bar_id)

            Kl = bar_object.local_stiffness_matrix()
            TM = bar_object.transformation_matrix()
            Kg = TM.T.dot(Kl).dot(TM)


            self.bar_Kl_dict[bar_id] = []
            self.bar_Kl_dict[bar_id].append(Kl)

            # build list of bar local stifness matrices to use in calculation of results

            K11 = Kg[0:6,0:6]
            K12 = Kg[0:6,6:12]
            K21 = Kg[6:12,0:6]
            K22 = Kg[6:12,6:12]


            for i in range (6):
                for j in range(6):

                    K11_data = K11[i,j]
                    K12_data = K12[i,j]
                    K21_data = K21[i,j]
                    K22_data = K22[i,j]

                    if(K11_data != 0):
                    
                        row_index_11 = int(i + 6*node_i_index)
                        col_index_11 = int(j + 6*node_i_index)

                        self.primarty_stiffness_matrix[row_index_11,col_index_11] = self.primarty_stiffness_matrix[row_index_11,col_index_11] + K11_data

                    if(K12_data != 0):

                        row_index_12 = int(i + 6*node_i_index)
                        col_index_12 = int(j + 6*node_j_index)

                        self.primarty_stiffness_matrix[row_index_12,col_index_12] = self.primarty_stiffness_matrix[row_index_12,col_index_12] + K12_data

                    if(K21_data != 0):

                        row_index_21 = int(i + 6*node_j_index)
                        col_index_21 = int(j + 6*node_i_index)

                        self.primarty_stiffness_matrix[row_index_21,col_index_21] = self.primarty_stiffness_matrix[row_index_21,col_index_21] + K21_data

                    if(K22_data != 0):

                        row_index_22 = int(i+ 6*node_j_index)
                        col_index_22 = int(j + 6*node_j_index)
                    
                        self.primarty_stiffness_matrix[row_index_22,col_index_22] = self.primarty_stiffness_matrix[row_index_22,col_index_22] + K22_data
        
        return self.primarty_stiffness_matrix

    def build_structural(self):

        support_cursor = self.model.connection.cursor()
        support_cursor.execute('SELECT * FROM element_support ORDER BY node_index ASC') 
        support_list = support_cursor.fetchall()


        #cycle through supports and build flag list
        for support in support_list:

            if( support[1] == 1) : self.removed_indices_list.append(int(support[0])*6+0)
            if( support[2] == 1) : self.removed_indices_list.append(int(support[0])*6+1)
            if( support[3] == 1) : self.removed_indices_list.append(int(support[0])*6+2)
            if( support[4] == 1) : self.removed_indices_list.append(int(support[0])*6+3)
            if( support[5] == 1) : self.removed_indices_list.append(int(support[0])*6+4)
            if( support[6] == 1) : self.removed_indices_list.append(int(support[0])*6+5)

        support_cursor.close()

        self.ndof_structure = self.ndof_primary - len(self.removed_indices_list)

        self.structual_stiffness_matrix = np.delete(self.primarty_stiffness_matrix, self.removed_indices_list,0)
        self.structual_stiffness_matrix = np.delete(self.structual_stiffness_matrix, self.removed_indices_list,1)

        return self.structual_stiffness_matrix

    def build_force_vector(self):

        self.force_vector = np.zeros((self.ndof_primary),dtype=np.int8)

        pointload_cursor = self.model.connection.cursor()
        pointload_cursor.execute('SELECT * FROM load_pointload') 

        for ptLoad in pointload_cursor:

            NodeIndex = ptLoad[0]

            if ptLoad[1] != 0: self.force_vector[NodeIndex*6] = ptLoad[1]*1000
            if ptLoad[2] != 0: self.force_vector[NodeIndex*6 + 1] = ptLoad[2]*1000
            if ptLoad[3] != 0: self.force_vector[NodeIndex*6 + 2] = ptLoad[3]*1000
            if ptLoad[4] != 0: self.force_vector[NodeIndex*6 + 3] = ptLoad[4]*1000
            if ptLoad[5] != 0: self.force_vector[NodeIndex*6 + 4] = ptLoad[5]*1000
            if ptLoad[6] != 0: self.force_vector[NodeIndex*6 + 5] = ptLoad[6]*1000

        pointload_cursor.close()

        self.force_vector = np.delete(self.force_vector, self.removed_indices_list, 0)

        return self.force_vector


        

