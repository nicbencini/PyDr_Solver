import numpy as np
from model import property

class node:

    def __init__(self,
                 x : float,
                 y : float,
                 z : float):

        self.x = x
        self.y = y
        self.z = z


class bar:

    def __init__(self,
                 node_a : node,
                 node_b : node,
                 section : property.section,
                 orientation_vector : np.array,
                 release_a : str = 'XXXXXX',
                 release_b : str = 'XXXXXX',
                 ):

        self.point_a = node_a
        self.point_b = node_b
        self.section = section
        self.orientation_vector = orientation_vector
        self.release_a = release_a
        self.release_b = release_b

