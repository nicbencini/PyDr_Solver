"""
This module contains the functions for the geometrical manipulation of vectors.
"""

import numpy as np

def solve(model):
    """
    This module contains the functions for the geometrical manipulation of vectors.
    """

    stiffness_matrix = StiffnessMatrix(model)

    stiffness_matrix.build_primary()
    stiffness_matrix.build_structural()
    stiffness_matrix.build_force_vector()
    stiffness_matrix.solve()
    stiffness_matrix.build_node_dispalcements()
    stiffness_matrix.build_node_reactions()


class StiffnessMatrix:
    """
    description of class
    """

    def __init__(self, model):

        self.model = model
        self.bar_kl_dict={}
        self.removed_indices_list = []
        self.flag_list = []
        self.ndof_structure = None
        self.structual_stiffness_matrix = None
        self.force_vector = None
        self.displacement_vector = []
        self.reaction_vector = None

        # Initiate primary stiffness matrix

        node_cursor = model.connection.cursor()
        self.node_id_list = node_cursor.execute('SELECT _id FROM element_node').fetchall()
        node_cursor.close()

        self.ndof_primary =  len(self.node_id_list) * 6

        if(self.ndof_primary ** 2)*8 > 1e+9:
            raise RuntimeError('Stiffness matrix size exceeds 1GB.'
                               + 'Reduce the number of elements in the model')

        self.primarty_stiffness_matrix = np.zeros((self.ndof_primary,
                                                   self.ndof_primary),
                                                   dtype=np.int8)



    def solve(self):
        """
        description of class
        """
        reduced_displacement_vector = np.linalg.solve(self.structual_stiffness_matrix,
                                                      self.force_vector)

        count = 0

        for flag in self.flag_list:

            if flag == 0:
                self.displacement_vector.append(reduced_displacement_vector[count])

                count += 1
            else:
                self.displacement_vector.append(0.0)

        self.reaction_vector = np.dot(self.primarty_stiffness_matrix,
                                      np.array(self.displacement_vector).T)


    def build_primary(self):
        """
        description of class
        """

        bar_cursor = self.model.connection.cursor()
        bar_cursor.execute('SELECT * FROM element_bar')

        for bar in bar_cursor:

            bar_id = bar[0]
            node_i_index  = bar[1]
            node_j_index  = bar[2]

            bar_object = self.model.get_bar(bar_id)

            kl = bar_object.local_stiffness_matrix()
            tm = bar_object.transformation_matrix()
            kg = tm.T.dot(kl).dot(tm)

            self.bar_kl_dict[bar_id] = []
            self.bar_kl_dict[bar_id].append(kl)

            # build list of bar local stifness matrices to use in calculation of results

            k11 = kg[0:6,0:6]
            k12 = kg[0:6,6:12]
            k21 = kg[6:12,0:6]
            k22 = kg[6:12,6:12]


            for i in range (6):
                for j in range(6):

                    k11_data = k11[i,j]
                    k12_data = k12[i,j]
                    k21_data = k21[i,j]
                    k22_data = k22[i,j]

                    if k11_data != 0:
                        row_index_11 = int(i + 6*node_i_index)
                        col_index_11 = int(j + 6*node_i_index)

                        self.primarty_stiffness_matrix[row_index_11,col_index_11] = self.primarty_stiffness_matrix[row_index_11,col_index_11] + k11_data

                    if k12_data != 0:

                        row_index_12 = int(i + 6*node_i_index)
                        col_index_12 = int(j + 6*node_j_index)

                        self.primarty_stiffness_matrix[row_index_12,col_index_12] = self.primarty_stiffness_matrix[row_index_12,col_index_12] + k12_data

                    if k21_data != 0:

                        row_index_21 = int(i + 6*node_j_index)
                        col_index_21 = int(j + 6*node_i_index)

                        self.primarty_stiffness_matrix[row_index_21,col_index_21] = self.primarty_stiffness_matrix[row_index_21,col_index_21] + k21_data

                    if k22_data != 0:

                        row_index_22 = int(i+ 6*node_j_index)
                        col_index_22 = int(j + 6*node_j_index)

                        self.primarty_stiffness_matrix[row_index_22,col_index_22] = self.primarty_stiffness_matrix[row_index_22,col_index_22] + k22_data

        return self.primarty_stiffness_matrix

    def build_structural(self):
        """
        description of class
        """

        support_cursor = self.model.connection.cursor()
        support_cursor.execute('SELECT * FROM element_support ORDER BY node_index ASC')
        support_list = support_cursor.fetchall()

        #cycle through supports and build flag list
        for support in support_list:

            if support[1] == 1 :
                self.removed_indices_list.append(int(support[0])*6+0)
            if support[2] == 1 :
                self.removed_indices_list.append(int(support[0])*6+1)
            if support[3] == 1 :
                self.removed_indices_list.append(int(support[0])*6+2)
            if support[4] == 1 :
                self.removed_indices_list.append(int(support[0])*6+3)
            if support[5] == 1 :
                self.removed_indices_list.append(int(support[0])*6+4)
            if support[6] == 1 :
                self.removed_indices_list.append(int(support[0])*6+5)

        support_cursor.close()

        self.flag_list = np.zeros(self.ndof_primary)
        self.flag_list[self.removed_indices_list] = -1

        self.ndof_structure = self.ndof_primary - len(self.removed_indices_list)
        self.structual_stiffness_matrix = np.delete(self.primarty_stiffness_matrix,
                                                    self.removed_indices_list,
                                                    0)
        self.structual_stiffness_matrix = np.delete(self.structual_stiffness_matrix,
                                                    self.removed_indices_list,
                                                    1)

        return self.structual_stiffness_matrix

    def build_force_vector(self):
        """
        description of class
        """

        self.force_vector = np.zeros((self.ndof_primary),dtype=np.int8)

        pointload_cursor = self.model.connection.cursor()
        pointload_cursor.execute('SELECT * FROM load_pointload')

        for pt_load in pointload_cursor:

            node_index = pt_load[0]

            if pt_load[1] != 0:
                self.force_vector[node_index*6] = pt_load[1]*1000
            if pt_load[2] != 0:
                self.force_vector[node_index*6 + 1] = pt_load[2]*1000
            if pt_load[3] != 0:
                self.force_vector[node_index*6 + 2] = pt_load[3]*1000
            if pt_load[4] != 0:
                self.force_vector[node_index*6 + 3] = pt_load[4]*1000
            if pt_load[5] != 0:
                self.force_vector[node_index*6 + 4] = pt_load[5]*1000
            if pt_load[6] != 0:
                self.force_vector[node_index*6 + 5] = pt_load[6]*1000

        pointload_cursor.close()

        self.force_vector = np.delete(self.force_vector, self.removed_indices_list, 0)

        return self.force_vector

    def build_node_dispalcements(self):
        """
        description of class
        """

        results_cursor = self.model.connection.cursor()

        results_cursor.execute("DELETE FROM result_node_displacement")

        for i in range(len(self.node_id_list)):

            node_id = self.node_id_list[i][0]
            ux = self.displacement_vector[node_id*6]
            uy = self.displacement_vector[node_id*6 + 1]
            uz = self.displacement_vector[node_id*6 + 2]
            rx = self.displacement_vector[node_id*6 + 3]
            ry = self.displacement_vector[node_id*6 + 4]
            rz = self.displacement_vector[node_id*6 + 5]

            results_node_displacement_string = (node_id,"",ux,uy,uz,rx,ry,rz)

            results_node_displacement_query = """INSERT INTO result_node_displacement
                                    (node_index, load_case, ux, uy, uz, rx, ry, rz) 
                                    VALUES 
                                    (?,?,?,?,?,?,?,?)"""

            results_cursor.execute(results_node_displacement_query,results_node_displacement_string)

        self.model.connection.commit()
        results_cursor.close()

    def build_node_reactions(self):
        """
        description of class
        """

        support_cursor = self.model.connection.cursor()
        support_id_list = support_cursor.execute('SELECT node_index FROM element_support').fetchall()
        support_cursor.close()

        results_cursor = self.model.connection.cursor()
        results_cursor.execute("DELETE FROM result_node_reactions")

        for i in range(len(support_id_list)):

            node_id = support_id_list[i][0]
            fx = self.reaction_vector[node_id*6 + 0]
            fy = self.reaction_vector[node_id*6 + 1]
            fz = self.reaction_vector[node_id*6 + 2]
            mx = self.reaction_vector[node_id*6 + 3]
            my = self.reaction_vector[node_id*6 + 4]
            mz = self.reaction_vector[node_id*6 + 5]

            results_node_reaction_string = (node_id,"",fx,fy,fz,mx,my,mz)

            results_node_reaction_query = """INSERT INTO result_node_reactions
                                    (node_index, load_case, fx, fy, fz, mx, my, mz) 
                                    VALUES 
                                    (?,?,?,?,?,?,?,?)"""

            results_cursor.execute(results_node_reaction_query,results_node_reaction_string)

        self.model.connection.commit()
        results_cursor.close()
