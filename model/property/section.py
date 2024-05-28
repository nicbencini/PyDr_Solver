
class section:

    def __init__ (self, 
                  name : str, 
                  material : str, 
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
                                  'steel',
                                  0.0123, # sqm
                                  0.0002225, # m^4
                                  0.00007308, # m^4
                                  )

        return default_section
        
section.default()
