import numpy as np
import uuid
from objects import property

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
                 ):

        self.node_a = node_a
        self.node_b = node_b
        self.section = section
        self.orientation_vector = orientation_vector
        self.release_a = release_a
        self.release_b = release_b
        self.id = str(uuid.uuid4())

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