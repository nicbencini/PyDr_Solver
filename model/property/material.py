
class material:

    def __init__ (self,
                  name : str,
                  youngs_modulus : float, # MPa
                  poissons_ratio : float,
                  shear_modulus : float, # MPa
                  coeff_thermal_expansion : float, # 1/c
                  damping_ratio : float,
                  density : float # kN/m^3
                  ):
        
        self.name = name
        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio
        self.shear_modulus = shear_modulus
        self.coeff_thermal_expansion = coeff_thermal_expansion
        self.damping_ratio = damping_ratio
        self.density = density
        
    @staticmethod

    def default():

        default_material = material('steel',
                                    210000, # MPa
                                    0.3,
                                    76903.07, # MPa
                                    0.0000117, # 1/c
                                    0,
                                    76.9729, # kN/m^3
                                    )
        
        return default_material
    
