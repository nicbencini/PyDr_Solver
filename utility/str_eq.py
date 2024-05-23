
class structural_equations:

    def axial_coeff(E : float,A : float,L : float):
        return E*A/L # Axial Force Coefficient

    def torsional_coeff(G,J,L):
        return G*J/L

    def coeff_1(E,I,L):
        return 12*E*I/L**3
    
    def coeff_2(E,I,L):
        return 6*E*I/L**2

    def coeff_3(E,I,L):
        return 6*E*I/L**2
    
    def coeff_4(E,I,L):
        return 4*E*I/L
    
    def coeff_5(E,I,L):
        return 2*E*I/L


