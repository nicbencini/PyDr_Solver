"""
This module contains the functions for the geometrical manipulation of vectors.
"""
import numpy as np
from objects import element # pylint: disable=import-error

class PointLoad:
    """
        Creates a point load object
    """
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

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

    def to_string(self):
        """Returns a string with the object variables."""

        return f'Load ({self.fx},{self.fy},{self.fz},{self.mx},{self.my},{self.mz})'

    def to_array(self):
        """Returns an array with the object variables."""

        return np.array([self.fx,
                         self.fy,
                         self.fz,
                         self.mx,
                         self.my,
                         self.mz])
