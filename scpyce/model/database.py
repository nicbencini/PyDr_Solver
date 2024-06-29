import sqlite3
import numpy as np
import warnings
from objects import properties
from objects import element
from model import tables
from model import write
from model import read

class Model:
    def __init__(self , file_path):
        self.database_path = file_path
        self.connection = sqlite3.connect(self.database_path)

        print(f'Connected to {self.database_path}')

    def build_tables(self):
        """
        Builds the tables for the model database.
        """

        #Build object tables
        tables.build_bar_table(self.connection)
        tables.build_node_table(self.connection)
        tables.build_support_table(self.connection)

        #Build property tables
        tables.build_material_table(self.connection)
        tables.build_section_table(self.connection)

        #Build load tables
        tables.build_point_load_table(self.connection)
        
        #Build results tables
        tables.build_node_displacements_table(self.connection)
        tables.build_node_reactions_table(self.connection)

    def add_bar(self, bar):
        """
        Adds a bar to the database. Returns the id of that bar. 
        If the bar already exists it will return the id of the existing bar.
        """
        write.add_bar(self, bar)
        
    def add_node(self, node):
        """
        Adds a node to the database. Returns the id of that node. 
        If the node already exists it will return the id of the existing node.
        """

        write.add_node(self, node)

    
    def add_material(self, material):
        """
        Adds a node to the database. Returns the node_index of that node. 
        If the node already exists it will return the node_index of the existing node.
        """

        write.add_material(self, material)

    def add_section(self, section):
        """
        Adds a node to the database. Returns the node_index of that node. 
        If the node already exists it will return the node_index of the existing node.
        """

        write.add_section(self,section)

    def add_support(self, support):
            """
            Adds a support to the database. Returns the id of the node of the support. 
            If the node already exists it will return the id of the existing node.
            """

            write.add_support(self, support)

    def add_point_load(self, pointload):
            """
            Adds a point load to the database. Returns the id of the node of the point load. 
            If the node already exists it will return the id of the existing node.
            """

            write.add_point_load(self, pointload)

    def get_material(self, material_name):

        
        material_object = read.get_material(self, material_name)

        return material_object

    def get_section(self, section_name):

        section_object = read.get_section(self, section_name)

        return section_object
    
    def get_node(self, node_index):
        
        node_object = read.get_node(self, node_index)

        return node_object
   
    def get_bar(self, bar_name):
        
        bar_object = read.get_bar(self, bar_name)
        
        return bar_object
    

    def close_connection(self):
        """
        Closes the connection to the model database. 
        IMPORTANT: this must be run to end work on the model.
        """

        self.connection.close()
        print( f'Connection to {self.database_path} closed')

