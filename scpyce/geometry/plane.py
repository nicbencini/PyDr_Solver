"""
This module contains the functions for the geometrical manipulation of planes.
"""

import numpy as np
from geometry import vector_3d # pylint: disable=import-error

@staticmethod

def plane_from_3pt(point_1, point_2, oreintation_vector, x_axis_oriented = True):
    """
    This function builds a plane from:

     -A point defining the start of a line
     -A point defining the end of a line
     -An orientation vector defining the orinetation of the x axis

     If the orientation vector defines the orientation of the y-axis 
     set the x_axis_oriented boolean to false.
    """

    origin = point_1
    x_vector = vector_3d.unit(point_2 - point_1)

    if vector_3d.is_parallel(x_vector , oreintation_vector):
        if not vector_3d.is_parallel(x_vector , vector_3d.unit_z):
            oreintation_vector = vector_3d.unit_z
        else:
            oreintation_vector = -vector_3d.unit_x


    y_vector = vector_3d.unit(vector_3d.gram_schmit(x_vector, oreintation_vector))

    z_vector = vector_3d.unit(np.cross(x_vector, y_vector))


    if not x_axis_oriented:
        x_vector , y_vector , z_vector = y_vector , z_vector, x_vector

    return origin , x_vector , y_vector , z_vector
