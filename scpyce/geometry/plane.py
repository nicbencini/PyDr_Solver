import numpy as np
import math
from geometry import vector_3d

@staticmethod

def plane_from_3pt(point_1, point_2, oreintation_vector, xAxisOrientedToLine = True):

    origin = point_1
    x_vector = vector_3d.unit(point_2 - point_1)

    if (vector_3d.is_parallel(x_vector , oreintation_vector)):
    
        if (not vector_3d.is_parallel(x_vector , vector_3d.unit_z)):

            oreintation_vector = vector_3d.unit_z

        else:

            oreintation_vector = -vector_3d.unit_x


    y_vector = vector_3d.unit(vector_3d.gram_schmit(x_vector, oreintation_vector))

    z_vector = vector_3d.unit(np.cross(x_vector, y_vector))


    if (not xAxisOrientedToLine):
        x_vector , y_vector , z_vector = y_vector , z_vector, x_vector

    return origin , x_vector , y_vector , z_vector