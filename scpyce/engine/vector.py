import numpy as np

class ForceVector(object):

    data_connection = None
    vector = None

    def __init__(self, data_connection):
        
        ForceVector.data_connection = data_connection

    def build(self, nDof_structure):

        force_vector_data = []
        force_vector_row = []
        force_vector_col = []
        
        pointload_cursor = ForceVector.data_connection.cursor()
        pointload_cursor.execute('SELECT * FROM load_pointload') 

        for ptLoad in pointload_cursor:

            NodeIndex = ptLoad[0]

            if ptLoad[1] != 0:
                    force_vector_data.append(ptLoad[1]*1000)
                    force_vector_row.append(NodeIndex*6)
                    force_vector_col.append(0)

            if ptLoad[2] != 0:
                    force_vector_data.append(ptLoad[2]*1000)
                    force_vector_row.append(NodeIndex*6 + 1)
                    force_vector_col.append(0)

            if ptLoad[3] != 0:
                    force_vector_data.append(ptLoad[3]*1000)
                    force_vector_row.append(NodeIndex*6 + 2)
                    force_vector_col.append(0)

            if ptLoad[4] != 0:
                    force_vector_data.append(ptLoad[4]*1000)
                    force_vector_row.append(NodeIndex*6 + 3)
                    force_vector_col.append(0)

            if ptLoad[5] != 0:
                    force_vector_data.append(ptLoad[5]*1000)
                    force_vector_row.append(NodeIndex*6 + 4)
                    force_vector_col.append(0)

            if ptLoad[6] != 0:
                    force_vector_data.append(ptLoad[6]*1000)
                    force_vector_row.append(NodeIndex*6 + 5)
                    force_vector_col.append(0)

        pointload_cursor.close()

        force_vector = csc_matrix((force_vector_data, (force_vector_row, force_vector_col)), shape = (nDof_structure, 1))

        ForceVector.vector = force_vector.toarray()

        print("Built Force Vector ....")