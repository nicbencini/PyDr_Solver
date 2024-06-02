import numpy as np
import math

class Vector:

    @staticmethod

    def magnitude(vector):

        return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)


    def unit_vector(vector):
       unit_vec = np.array([vector[0] / Vector.magnitude(vector), 
                            vector[1] / Vector.magnitude(vector), 
                            vector[2] / Vector.magnitude(vector)])
       
       return unit_vec
    
    def gram_schmit(vector_1, vector_2):
        """Creates an orthogonal vector to the first vector in a plane defined by both vectors"""

        return vector_2 - (np.dot(vector_2,vector_1)*vector_1)

    def is_parallel(vector_1, vector_2):
       
       return np.dot(vector_1,vector_2) == 0
    
    def unit_x():
       return np.array([1,0,0])
    
    def unit_y():
       return np.array([0,1,0])
    
    def unit_z():
       return np.array([0,0,1])

class Plane:

    def plane_from_3pt(point_1, point_2, oreintation_vector, xAxisOrientedToLine = True):

        origin = point_1
        x_vector = point_2 - Vector.unit_vector(point_1)

        if (Vector.is_parallel(x_vector , oreintation_vector)):
        
            if (Vector.is_parallel(x_vector , Vector.unit_z)):

                oreintation_vector = Vector.unit_z

            else:

                oreintation_vector = -Vector.unit_x


        y_vector = Vector.unit_vector(Vector.gram_schmit(x_vector, oreintation_vector))

        z_vector = Vector.unit_vector(np.cross(x_vector, y_vector))


        if (not xAxisOrientedToLine):
            x_vector , y_vector , z_vector = y_vector , z_vector, x_vector

        return origin , x_vector , y_vector , z_vector

        

        
     
