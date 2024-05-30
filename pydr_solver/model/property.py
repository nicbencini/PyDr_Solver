import numpy as np

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

class section:

    def __init__ (self,
                  name : str,
                  material : material,
                  area : float, # sqm
                  izz : float, # m^4
                  iyy : float, # m^4
                  ):

        self.name = name
        self.material = material
        self.area = area
        self.izz = izz
        self.iyy = iyy
        self.ip = izz + iyy

    @staticmethod

    def default():

        default_section = section('UC305x305x970',
                                  material.default(),
                                  0.0123, # sqm
                                  0.0002225, # m^4
                                  0.00007308, # m^4
                                  )

        return default_section

class local_plane:

    def __init__(self,
                 origin : np.array,
                 x_vector : np.array,
                 y_vector : np.array,
                 z_vector : np.array
                 ):
        
        self.origin = origin
        self.x_vector = x_vector
        self.y_vector = y_vector
        self.z_vector = z_vector





