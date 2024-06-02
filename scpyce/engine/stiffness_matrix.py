import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import numpy as np
import sqlite3
from objects import element
from objects import property

class LocalStiffnessMatrix:

    
    def build_local_stiffness_matrix(bar : element.Bar):
        

        section = bar.section
        material = section.material

        A = section.A 
        E = material.E 
        Iz = section.Iz
        Iy = section.Iy 
        G =  material.G
        J =  material.J
        L = bar.L 

        release_a = bar.release_a
        release_b = bar.release_a
        local_plane = bar.local_plane

        # Axial coefficient
        a1 = E*A/L 
        
        #Torsional coefficient
        t1 = G*J/L

        #Shear coeffiecient - Major Axis
        v1 = 12*E*Iz/L**3
        v2 = 6*E*Iz/L**2

        #Shear coeffiecient - Minor Axis
        v3 = 12*E*Iy/L**3
        v4 = 6*E*Iy/L**2
        
        #Moment coeffiecient - Major Axis
        m1 = 6*E*Iz/L**2
        m2 = 4*E*Iz/L
        m3 = 2*E*Iz/L

        #Moment coeffiecient - Minor Axis
        m4 = 6*E*Iy/L**2
        m5 = 4*E*Iy/L
        m6 = 2*E*Iy/L

    
        #Build local stiffness matrix
        kl = [[  a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
              [ 0.0 ,  v1 , 0.0 , 0.0 , 0.0 , -m1 , 0.0 , -v1 , 0.0 , 0.0 , 0.0 , -m1 ],
              [ 0.0 , 0.0 ,  v3 , 0.0 ,  m4 , 0.0 , 0.0 , 0.0 , -v3 , 0.0 ,  m4 , 0.0 ],
              [ 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 ],
              [ 0.0 , 0.0 ,  v4 , 0.0 ,  m5 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m6 , 0.0 ],
              [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m2 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m3 ],
              [ -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , a1  , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
              [ 0.0 , -v1 , 0.0 , 0.0 , 0.0 ,  m1 , 0.0 ,  v1 , 0.0 , 0.0 , 0.0 ,  m1 ],
              [ 0.0 , 0.0 , -v3 , 0.0 , -m4 , 0.0 , 0.0 , 0.0 ,  v3 , 0.0 , -m4 , 0.0 ],
              [ 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 ],
              [ 0.0 , 0.0 ,  v4 , 0.0 ,  m5 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m6 , 0.0 ],
              [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m2 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m3 ],
              ]

        #Build the full transformation matrix for this element
        TM = np.zeros((12,12))

        T_repeat =  np.array([list(local_plane.XVector.values()),
                              list(local_plane.YVector.values()),
                              list(local_plane.ZVector.values())]
                              )
        
        TM[0:3,0:3] = T_repeat
        TM[3:6,3:6] = T_repeat
        TM[6:9,6:9] = T_repeat
        TM[9:12,9:12] = T_repeat

        #Remove released coefficients
        
        combined_release_string = release_a + release_b

        count = 0

        for char in combined_release_string:

            if (char == "F"):

                divisor = Kl[count,count]

                row_values = np.divide(Kl[count,:],divisor)
                col_values = Kl[:,count]

                subtraction_vector = np.outer(col_values,row_values)

                Kl = np.subtract(Kl,subtraction_vector)
               

            count += 1

        #Build Global stiffness matrix
        Kg = TM.T.dot(Kl).dot(TM) 

class GlobalStiffnessMatrix:

    """description of class"""

    nDof_structure = None
    primary_stiffness_matrix = None
    structural_stiffness_matrix = None
    bar_Kl_dict={}
    bar_TM_dict={}
    flag_list=[]

    primary_matrix_data = []
    primary_matrix_row = []
    primary_matrix_col = []

    removed_indices_list = []


    def __init__(self, model):

        
        self.model = model

        node_cursor = model.connection.cursor()
        node_id_list = node_cursor.execute('SELECT _id FROM element_node').fetchall()

        self.ndof_primary =  len(node_id_list)*6
        node_cursor.close()


    def build_primary(self):

        bar_cursor = self.model.connection.cursor()
        bar_Update_cursor = self.model.connection.cursor()
        bar_cursor.execute('SELECT * FROM element_bar') 
        
        bar_divs = 4

        count = 0

        node_index_counter = (StiffnessMatrix.nDof_primary/6) - 1

        for bar in bar_cursor:

            bar_id = bar[0]
            bar_start_index = bar[1]
            bar_end_index = bar[2]
            sub_nodes_dict = {}
            

            section_name = (str(bar[4]),)

            section_cursor = StiffnessMatrix.data_connection.cursor()
            section = section_cursor.execute("SELECT * FROM property_section WHERE _id = ?",section_name).fetchone()
            section_cursor.close()

            material_name = (str(section[1]),)

            material_cursor = StiffnessMatrix.data_connection.cursor()
            material = material_cursor.execute("SELECT * FROM property_material WHERE _id = ?",material_name).fetchone()
            material_cursor.close()

            StiffnessMatrix.bar_Kl_dict[bar_id] = []
            
            for k in range(bar_divs):

                node_i_index = None
                node_j_index = None
                release_a = None
                release_b = None

                if k == 0:
                    node_i_index = bar_start_index
                    sub_nodes_dict[str(0)] = int(bar_start_index)
                    release_a = bar[6]
                else:
                    node_i_index = node_index_counter
                    sub_nodes_dict[str(k/bar_divs)] = int(node_i_index)
                    release_a = "XXXXXX"

                if k == (bar_divs - 1):
                    node_j_index = bar_end_index
                    sub_nodes_dict[str(1)] = int(bar_end_index)
                    release_b = bar[7]
                else:
                    node_j_index = node_index_counter + 1
                    node_index_counter += 1

                    

                    release_b = "XXXXXX"

                    for z in range (6):
                        StiffnessMatrix.nDof_primary += 1

               
                
                bar_stiffness_matrix = LocalStiffnessMatrix(bar, section, release_a, release_b,  material, bar_divs)

                bar_stiffness_matrix.Generate()


                Kl = bar_stiffness_matrix.Kl
                Kg = bar_stiffness_matrix.Kg
    
                StiffnessMatrix.bar_Kl_dict[bar_id].append(Kl)
                #StiffnessMatrix.bar_TM_dict[bar_id].append(Kl)
                     
                """
                if count == 0:  
                    bar_stiffness_matrix.plot_Kl()
                    bar_stiffness_matrix.plot_Kg()
                count += 1
                """
                
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

                            StiffnessMatrix.primary_matrix_data.append(K11_data) 
                            StiffnessMatrix.primary_matrix_row.append(row_index_11)
                            StiffnessMatrix.primary_matrix_col.append(col_index_11)


                        if(K12_data != 0):

                            row_index_12 = int(i + 6*node_i_index)
                            col_index_12 = int(j + 6*node_j_index)

                            StiffnessMatrix.primary_matrix_data.append(K12_data) 
                            StiffnessMatrix.primary_matrix_row.append(row_index_12)
                            StiffnessMatrix.primary_matrix_col.append(col_index_12)

                        if(K21_data != 0):

                            row_index_21 = int(i + 6*node_j_index)
                            col_index_21 = int(j + 6*node_i_index)

                            StiffnessMatrix.primary_matrix_data.append(K21_data) 
                            StiffnessMatrix.primary_matrix_row.append(row_index_21)
                            StiffnessMatrix.primary_matrix_col.append(col_index_21)

                        if(K22_data != 0):

                            row_index_22 = int(i+ 6*node_j_index)
                            col_index_22 = int(j + 6*node_j_index)
                        

                            StiffnessMatrix.primary_matrix_data.append(K22_data) 
                            StiffnessMatrix.primary_matrix_row.append(row_index_22)
                            StiffnessMatrix.primary_matrix_col.append(col_index_22)


            subnode_json_data = json.dumps(sub_nodes_dict)

            sqlite_insert_query = """UPDATE element_bar SET sub_nodes = ? WHERE _id = ?"""

            result_string = (subnode_json_data, bar_id)
            
            bar_Update_cursor.execute(sqlite_insert_query,result_string)

        bar_cursor.close()
        bar_Update_cursor.close()

        Ks = csc_matrix((StiffnessMatrix.primary_matrix_data, (StiffnessMatrix.primary_matrix_row, StiffnessMatrix.primary_matrix_col)), shape = (StiffnessMatrix.nDof_primary , StiffnessMatrix.nDof_primary ))

        #Ks = Ks[Ks.getnnz(1)>0][:,Ks.getnnz(0)>0]

        StiffnessMatrix.primary_stiffness_matrix = Ks

        print(node_index_counter)

        print("Built Stiffness Matrix ....")

class StructuralStiffnessMatrix:
    def build_structural(self):


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



