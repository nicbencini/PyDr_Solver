import numpy as np
import uuid
from objects import property
from geometry import vector_3d
from geometry import plane

class Node:
    """
        Creates a node object.
    """

    def __init__(self,
                 x : float,
                 y : float,
                 z : float):

        self.x = x
        self.y = y
        self.z = z


    def to_string(self):
        return f'Node at ({self.x},{self.y},{self.z})'
    
    def to_array(self):
        return np.array([self.x,self.y,self.z])


class Bar:
    """
        Creates a bar object.
    """

    def __init__(self,
                 node_a : Node,
                 node_b : Node,
                 section : property.Section,
                 orientation_vector : np.array,
                 release_a : str = 'XXXXXX',
                 release_b : str = 'XXXXXX',
                 id : str = None
                 ):

        self.node_a = node_a
        self.node_b = node_b
        self.section = section
        self.orientation_vector = orientation_vector
        self.release_a = release_a
        self.release_b = release_b
        self.id = id if id is not None else str(uuid.uuid4())
        self.length = vector_3d.length(node_a.to_array(),node_b.to_array())


    def local_stiffness_matrix(self):
        
        A = self.section.area
        E = self.section.material.youngs_modulus * 1000000 #FIX UNITS
        Iz = self.section.izz
        Iy = self.section.iyy
        G =  self.section.material.shear_modulus * 1000000 #FIX UNITS
        J =  Iz + Iy
        L = self.length

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
        Kl = [[  a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
                [ 0.0 ,  v1 , 0.0 , 0.0 , 0.0 , -m1 , 0.0 , -v1 , 0.0 , 0.0 , 0.0 , -m1 ],
                [ 0.0 , 0.0 ,  v3 , 0.0 ,  m4 , 0.0 , 0.0 , 0.0 , -v3 , 0.0 ,  m4 , 0.0 ],
                [ 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 ],
                [ 0.0 , 0.0 ,  v4 , 0.0 ,  m5 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m6 , 0.0 ],
                [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m2 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m3 ],
                [ -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , a1  , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
                [ 0.0 , -v1 , 0.0 , 0.0 , 0.0 ,  m1 , 0.0 ,  v1 , 0.0 , 0.0 , 0.0 ,  m1 ],
                [ 0.0 , 0.0 , -v3 , 0.0 , -m4 , 0.0 , 0.0 , 0.0 ,  v3 , 0.0 , -m4 , 0.0 ],
                [ 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 ],
                [ 0.0 , 0.0 ,  v4 , 0.0 ,  m6 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m5 , 0.0 ],
                [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m3 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m2 ],
                ]


        #Remove released coefficients
        
        combined_release_string = self.release_a + self.release_b

        count = 0

        for char in combined_release_string:

            if (char == "F"):

                divisor = Kl[count,count]

                row_values = np.divide(Kl[count,:],divisor)
                col_values = Kl[:,count]

                subtraction_vector = np.outer(col_values,row_values)

                Kl = np.subtract(Kl,subtraction_vector)
                

            count += 1

        return Kl

    def transformation_matrix(self):

        #Build the full transformation matrix for this element
        TM = np.zeros((12,12))

        local_plane = plane.plane_from_3pt(self.node_a.to_array(),
                                                       self.node_b.to_array(), 
                                                       self.orientation_vector, 
                                                       True
                                                       )

        T_repeat =  np.array([local_plane[1],
                            local_plane[2],
                            local_plane[3]]
                            )
        

        TM[0:3,0:3] = T_repeat
        TM[3:6,3:6] = T_repeat
        TM[6:9,6:9] = T_repeat
        TM[9:12,9:12] = T_repeat

        return TM


class Support:
    """
        Creates a 6 degeree of freedom node support object. 
        Each degree of freedom is represented by a bool.
        True = fixed, False = released.
    """
    
    def __init__(self, 
                 node : Node,
                 fx : bool,
                 fy : bool,
                 fz : bool,
                 mx : bool,
                 my : bool,
                 mz : bool                 
                 ):
        
        self.node = node
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz

    def set_fix(self):
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = True
        self.my = True
        self.mz = True

    def set_pin(self):
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = False
        self.my = False
        self.mz = False

    @staticmethod

    def pin(node):
        return Support(node,True,True,True,False,False,False)
    
    def fix(node):
        return Support(node,True,True,True,True,True,True)