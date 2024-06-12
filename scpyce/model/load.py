from model import element

class PointLoad:
    """
        Creates a point load object
    """
    
    def __init__(self, 
                 node : element.Node,
                 fx : float,
                 fy : float,
                 fz : float,
                 mx : float,
                 my : float,
                 mz : float                 
                 ):
        
        self.node = node
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz