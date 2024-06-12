import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import numpy as np
import sqlite3
from model import element
from model import property
from util import vector_math


class GlobalStiffnessMatrix:

    """description of class"""

    def __init__(self, model):

        node_cursor = model.connection.cursor()
        node_id_list = node_cursor.execute('SELECT _id FROM element_node').fetchall()
        node_cursor.close()

        self.model = model
        self.ndof_primary =  len(node_id_list)
        self.nDof_structure = None

        self.bar_Kl_dict={}
        self.flag_list=[]
        self.removed_indices_list = []


        if((self.ndof_primary ** 2)*8 > 1e+9):
            raise RuntimeError('Stiffness matrix size exceeds 1GB. Reduce the number of elements in the model')
        else:
            self.primarty_stiffness_matrix = np.zeros((self.ndof_primary,self.ndof_primary),dtype=np.int8)

    def primary_stiffness_matrix(self):

        bar_cursor = self.model.connection.cursor()
        bar_cursor.execute('SELECT * FROM element_bar') 

        for bar in bar_cursor:

            bar_id = bar[0]
            node_i_index  = bar[1]
            node_j_index  = bar[2]

            section_name = (str(bar[4]),)

            ##WORKING HERE###
            bar[3] = section_object
            bar_object = element.Bar(*bar)


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





    def structural_stiffness_matrix(self):


        support_cursor = StiffnessMatrix.data_connection.cursor()
        support_cursor.execute('SELECT * FROM element_support ORDER BY node_index ASC') 
        support_list = support_cursor.fetchall()

        structural_matrix_data = []
        structural_matrix_row = []
        structural_matrix_col = []


        StiffnessMatrix.nDof_structure = StiffnessMatrix.nDof_primary

        #cycle through supports and build flag list
        for support in support_list:

            if( support[1] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+0)
            if( support[2] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+1)
            if( support[3] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+2)
            if( support[4] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+3)
            if( support[5] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+4)
            if( support[6] == 1) : StiffnessMatrix.removed_indices_list.append(int(support[0])*6+5)

        support_cursor.close()

        zero_row_check = np.diff(StiffnessMatrix.primary_stiffness_matrix.indptr) != 0
        

        index_count = 0

        for i in range(len(zero_row_check)):
            
            if (i in StiffnessMatrix.removed_indices_list):
                StiffnessMatrix.flag_list.append(-1)
                StiffnessMatrix.nDof_structure -= 1
            
            elif (not zero_row_check[i]):
                StiffnessMatrix.removed_indices_list.append(i)

                StiffnessMatrix.flag_list.append(-1)
                StiffnessMatrix.nDof_structure -= 1

            else:
                StiffnessMatrix.flag_list.append(index_count)
                index_count += 1




        for i in range (len(StiffnessMatrix.primary_matrix_data)):

            data = StiffnessMatrix.primary_matrix_data[i]
            row_index = StiffnessMatrix.primary_matrix_row[i]
            col_index = StiffnessMatrix.primary_matrix_col[i]

            if (StiffnessMatrix.flag_list[row_index] != -1) and (StiffnessMatrix.flag_list[col_index] != -1):

                structural_matrix_data.append(data)
                structural_matrix_row.append(StiffnessMatrix.flag_list[row_index])
                structural_matrix_col.append(StiffnessMatrix.flag_list[col_index])



        StiffnessMatrix.structural_stiffness_matrix = csc_matrix((structural_matrix_data, (structural_matrix_row, structural_matrix_col)), shape = (StiffnessMatrix.nDof_structure , StiffnessMatrix.nDof_structure ))



