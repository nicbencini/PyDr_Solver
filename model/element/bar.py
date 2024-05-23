

class bar:

    def __init__(self, _id : str, 
                 point_a : int, 
                 point_b : int, 
                 length : float, 
                 section : str = 'default' , 
                 local_plane : str = None, 
                 release_a : str = 'XXXXXX', 
                 release_b : str = 'XXXXXX', 
                 sub_nodes : str = None):
        
        self._id = _id
        self.point_a = point_a
        self.point_b = point_b
        self.length = length
        self.section = section
        self.local_plane = local_plane
        self.release_a = release_a
        self.release_b = release_b
        self.sub_nodes = sub_nodes



