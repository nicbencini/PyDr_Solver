

class local_stiffness_matrix:

    def axial_coeff(E : float,A : float,L : float):
        # Axial force at support
        return E*A/L 

    def torsional_coeff(G,J,L):
        # Torsional reaction at support
        return G*J/L

    def translation_shear_coeff(E,I,L):
        # Shear reaction developing at support due to translation
        return 12*E*I/L**3
    
    def translation_moment_coeff(E,I,L):
        # Moment reaction developing at support due to translation
        return 6*E*I/L**2

    def rotation_shear_coeff(E,I,L):
        # Shear reaction developing at support due to rotation
        return 6*E*I/L**2
    
    def rotation_moment_coeff_1(E,I,L):
        # Moment reaction developing at support due to rotation (rotated node)
        return 4*E*I/L
    
    def rotation_moment_coeff_2(E,I,L):
        # Moment reaction developing at support due to rotation (stationary node)
        return 2*E*I/L
    

    


