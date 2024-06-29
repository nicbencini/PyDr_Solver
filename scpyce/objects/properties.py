"""
This module contains the functions for the geometrical manipulation of vectors.
"""
import numpy as np

class Material:
    """
    This module contains the functions for the geometrical manipulation of vectors.
    """
    # pylint: disable=too-many-instance-attributes
    # Eleven is reasonable in this case.

    def __init__ (self,
                  name : str,
                  youngs_modulus : float, # MPa
                  poissons_ratio : float,
                  shear_modulus : float, # MPa
                  coeff_thermal_expansion : float, # 1/c
                  damping_ratio : float,
                  density : float, # kN/m^3
                  type : str = None, # pylint: disable=redefined-builtin
                  region: str = None,
                  embodied_carbon : float = None #kgCO2e/m^3
                  ):

        # pylint: disable=too-many-arguments
        # Eleven is reasonable in this case.

        self.name = name
        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio
        self.shear_modulus = shear_modulus
        self.coeff_thermal_expansion = coeff_thermal_expansion
        self.damping_ratio = damping_ratio
        self.density = density
        self.type = type
        self.region = region
        self.embodied_carbon = embodied_carbon

    @staticmethod

    def default():
        """This module contains the functions for the geometrical manipulation of vectors."""

        default_material = Material('steel',
                                    210000, # MPa
                                    0.3,
                                    76903.07, # MPa
                                    0.0000117, # 1/c
                                    0,
                                    76.9729, # kN/m^3
                                    'STEEL',
                                    'UK',
                                    12090 #kgCO2e/m^3
                                    )

        return default_material

    def to_string(self):
        """Returns a string with the object variables."""

        return f'Material: name = {self.name}'

    def to_array(self):
        """Returns an array with the object variables."""

        return np.array([self.name,
                         self.youngs_modulus,
                         self.poissons_ratio,
                         self.shear_modulus,
                         self.coeff_thermal_expansion,
                         self.damping_ratio,
                         self.density,
                         self.type,
                         self.region,
                         self.embodied_carbon
                        ]
                        )

class Section:
    """
    This module contains the functions for the geometrical manipulation of vectors.
    """
    # pylint: disable=too-many-arguments
    # Six is reasonable in this case.

    def __init__ (self,
                  name : str,
                  material : Material,
                  area : float, # sqm
                  izz : float, # m^4
                  iyy : float, # m^4
                  ):

        self.name = name
        self.material = material
        self.area = area
        self.izz = izz
        self.iyy = iyy

    @staticmethod

    def default():
        """This module contains the functions for the geometrical manipulation of vectors."""

        default_section = Section('UC305x305x97',
                                  Material.default(),
                                  0.0123, # sqm
                                  0.0002225, # m^4
                                  0.00007308, # m^4
                                  )

        return default_section

    def to_string(self):
        """Returns a string with the object variables."""

        return f'Section: name = {self.name}'

    def to_array(self):
        """Returns an array with the object variables."""

        return np.array([self.name,
                         self.material.name,
                         self.area,
                         self.izz,
                         self.iyy]
                         )

class LocalPlane:
    """
    This module contains the functions for the geometrical manipulation of vectors.
    """

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

    def to_string(self):
        """Returns a string with the object variables."""

        return f'Local Plane at {self.origin}'

    def to_array(self):
        """Returns an array with the object variables."""

        return np.array([self.origin,
                         self.x_vector,
                         self.y_vector,
                         self.z_vector]
                         )
