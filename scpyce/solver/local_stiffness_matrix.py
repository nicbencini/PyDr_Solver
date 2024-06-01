import os
import sys


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import numpy as np
import model.element as elm
import model.property as prp

class local_stiffness_matrix:

    
    def build_local_stiffness_matrix(bar : elm.bar):
        

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



