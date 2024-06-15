import sqlite3
import numpy as np
import warnings
from objects import property
from objects import element

class Model:
    def __init__(self , file_path):
        self.database_path = file_path
        self.connection = sqlite3.connect(self.database_path)

        print(f'Connected to {self.database_path}')

    def build_tables(self):
        """
        Builds the tables for the model database.
        """
        # create a database cursor
        cur = self.connection.cursor()

        # create the database table if it doesn't exist
        bar_table_schema = """
        CREATE TABLE IF NOT EXISTS element_bar (
            _id TEXT PRIMARY KEY,
            node_a INTEGER NOT NULL,
            node_b INTEGER NOT NULL,
            section TEXT NOT NULL,
            orientation_vector TEXT NOT NULL,
            release_a TEXT NOT NULL,
            release_b TEXT NOT NULL
        );
        """
        
        node_table_schema = """
        CREATE TABLE IF NOT EXISTS element_node (
            _id INTEGER NOT NULL,
            x FLOAT NOT NULL,
            y FLOAT NOT NULL,
            z FLOAT NOT NULL
        );
        """

        support_table_schema = """
        CREATE TABLE IF NOT EXISTS element_support (
            node_index INTEGER NOT NULL,
            fx INTEGER NOT NULL,
            fy INTEGER NOT NULL,
            fz INTEGER NOT NULL,
            mx INTEGER NOT NULL,
            my INTEGER NOT NULL,
            mz INTEGER NOT NULL
        );
        """

        point_load_table_schema = """
        CREATE TABLE IF NOT EXISTS load_pointload (
            node_index INTEGER NOT NULL,
            fx FLOAT NOT NULL,
            fy FLOAT NOT NULL,
            fz FLOAT NOT NULL,
            mx FLOAT NOT NULL,
            my FLOAT NOT NULL,
            mz FLOAT NOT NULL
        );
        """

        section_table_schema = """
        CREATE TABLE IF NOT EXISTS property_section (
            _id TEXT PRIMARY KEY,
            material TEXT NOT NULL,
            area FLOAT NOT NULL,
            izz FLOAT NOT NULL,
            iyy FLOAT NOT NULL
        );
        """

        material_table_schema = """
        CREATE TABLE IF NOT EXISTS property_material (
            _id TEXT PRIMARY KEY,
            youngs_modulus FLOAT NOT NULL,
            poissons_ratio FLOAT NOT NULL,
            shear_modulus FLOAT NOT NULL,
            coeff_thermal_expansion FLOAT NOT NULL,
            damping_ratio FLOAT NOT NULL,
            density FLOAT NOT NULL,
            type TEXT,
            region TEXT,
            embodied_carbon FLOAT
        );
        """

        cur.execute(bar_table_schema)
        cur.execute(node_table_schema)
        cur.execute(support_table_schema)
        cur.execute(point_load_table_schema)
        cur.execute(material_table_schema)
        cur.execute(material_table_schema)
        cur.execute(section_table_schema)

        cur.close()

    def add_bar(self, bar):
        """
        Adds a bar to the database. Returns the id of that bar. 
        If the bar already exists it will return the id of the existing bar.
        """
        bar_id = None

        cur = self.connection.cursor()

        node_a_index = self.add_node(bar.node_a)
        node_b_index = self.add_node(bar.node_b)

        bar_check_query = """
            SELECT _id 
            FROM element_bar
            WHERE (node_a = ?)
            AND (node_b = ?)
            """
        
        bar_check_result = cur.execute(bar_check_query,(node_a_index, node_b_index)).fetchone()


        if bar_check_result is not None:

            bar_id = bar_check_result[0]
            warnings.warn(f'Bar not added because of overlap with bar {bar_id}.')
        
        else:

            self.add_section(bar.section) # add section to database

            bar_query = """
            INSERT INTO element_bar (
                _id, node_a, node_b, section, orientation_vector, release_a, release_b) 
                VALUES 
                (?,?,?,?,?,?,?)
                """
            
            bar_value_string = (bar.id, node_a_index, node_b_index, bar.section.name, np.array2string(bar.orientation_vector), bar.release_a, bar.release_b)

            cur.execute(bar_query, bar_value_string)

            bar_id = bar.id


        self.connection.commit()

        cur.close()

        return bar_id
        
    def add_node(self, node):
        """
        Adds a node to the database. Returns the id of that node. 
        If the node already exists it will return the id of the existing node.
        """

        node_index = None

        cur = self.connection.cursor()

        node_check_query = """
            SELECT _id
            FROM element_node
            WHERE (x = ?)
            AND (y = ?)
            AND (z = ?)
            """

        node_check_result = cur.execute(node_check_query,(node.x, node.y, node.z)).fetchone()

        if node_check_result is not None:

            node_index = node_check_result[0]


        else:
            
            node_index = cur.execute("SELECT COUNT(*) FROM element_node").fetchone()[0]

            node_query = """
            INSERT INTO element_node (
                _id, x, y, z) 
                VALUES 
                (?,?,?,?)
                """
            
            node_value_string = (node_index, node.x, node.y, node.z)

            cur.execute(node_query, node_value_string)


        self.connection.commit()

        cur.close()

        return node_index
    
    def add_material(self, material):
        """
        Adds a node to the database. Returns the node_index of that node. 
        If the node already exists it will return the node_index of the existing node.
        """

        material_name = None

        cur = self.connection.cursor()

        material_check_query = """
            SELECT _id 
            FROM property_material
            WHERE (_id = ?)
            """

        material_check_result = cur.execute(material_check_query,[material.name]).fetchone()

        if material_check_result is not None:

            material_name = material_check_result[0]

        else:

            material_query = """
            INSERT INTO property_material (
                _id, youngs_modulus, poissons_ratio, shear_modulus, 
                coeff_thermal_expansion, damping_ratio,
                density, type, region, embodied_carbon) 
                VALUES 
                (?,?,?,?,?,?,?,?,?,?)
                """
            
            material_value_string = (material.name, material.youngs_modulus, material.poissons_ratio, 
                                 material.shear_modulus, material.coeff_thermal_expansion,
                                material.damping_ratio, material.density, material.type,
                                material.region, material.embodied_carbon)

            cur.execute(material_query, material_value_string)

            material_name = material.name


        self.connection.commit()

        cur.close()

        return material_name

    def add_section(self, section):
        """
        Adds a node to the database. Returns the node_index of that node. 
        If the node already exists it will return the node_index of the existing node.
        """

        section_name = None

        cur = self.connection.cursor()

        section_check_query = """
            SELECT _id 
            FROM property_section
            WHERE (_id = ?)
            """

        section_check_result = cur.execute(section_check_query, [section.name]).fetchone()

        if section_check_result is not None:

            section_name = section_check_result[0]

        else:

            self.add_material(section.material) # add material to database

            section_query = """
            INSERT INTO property_section (
                _id, material, area, izz, iyy) 
                VALUES 
                (?,?,?,?,?)
                """
            
            section_value_string = (section.name, section.material.name, section.area, section.izz, section.iyy)

            cur.execute(section_query, section_value_string)

            section_name = section.name

        self.connection.commit()

        cur.close()

        return section_name

    def add_support(self, support):
            """
            Adds a support to the database. Returns the id of the node of the support. 
            If the node already exists it will return the id of the existing node.
            """

            node_index = None

            cur = self.connection.cursor()

            support_check_query = """
                SELECT node_index
                FROM element_support
                WHERE (node_index = ?)
                """

            node_index = self.add_node(support.node)

            support_check_result = cur.execute(support_check_query, [node_index]).fetchone()

            if support_check_result is not None:

                support_index = support_check_result[0]

            else:

                support_query = """
                INSERT INTO element_support (
                    node_index, fx, fy, fz, mx, my, mz) 
                    VALUES 
                    (?,?,?,?,?,?,?)
                    """
                
                support_value_string = (node_index, support.fx, support.fy, support.fz, support.mx, support.my, support.mz)

                cur.execute(support_query, support_value_string)


            self.connection.commit()

            cur.close()

            return node_index

    def add_point_load(self, pointload):
            """
            Adds a point load to the database. Returns the id of the node of the point load. 
            If the node already exists it will return the id of the existing node.
            """

            node_index = None

            cur = self.connection.cursor()

            pointload_check_query = """
                SELECT node_index
                FROM load_pointload
                WHERE (node_index = ?)
                """

            node_index = self.add_node(pointload.node)

            pointload_check_result = cur.execute(pointload_check_query, [node_index]).fetchone()

            if pointload_check_result is not None:

                pointload_index = pointload_check_result[0]

            else:

                pointload_query = """
                INSERT INTO load_pointload (
                    node_index, fx, fy, fz, mx, my, mz) 
                    VALUES 
                    (?,?,?,?,?,?,?)
                    """
                
                pointload_value_string = (node_index, pointload.fx, pointload.fy, pointload.fz, pointload.mx, pointload.my, pointload.mz)

                cur.execute(pointload_query, pointload_value_string)


            self.connection.commit()

            cur.close()

            return node_index

    def get_material(self, material_name):

        material_cursor = self.connection.cursor()
        material_data = material_cursor.execute("SELECT * FROM property_material WHERE _id = ?",[material_name]).fetchone()
        material_object = property.Material(*material_data)
        material_cursor.close()

        return material_object

    def get_section(self, section_name):

        section_cursor = self.connection.cursor()
        section_data = section_cursor.execute("SELECT * FROM property_section WHERE _id = ?",[section_name]).fetchone()
        section_data = list(section_data)
        section_data[1] = self.get_material(section_data[1])
        section_object = property.Section(*section_data)
        section_cursor.close()

        return section_object
    
    def get_node(self, node_index):
        node_cursor = self.connection.cursor()
        node_data = node_cursor.execute("SELECT * FROM element_node LIMIT 1 OFFSET ?",[int(node_index)]).fetchone()

        node_object = element.Node(node_data[1], 
                                   node_data[2], 
                                   node_data[3])
        
        node_cursor.close()

        return node_object
        

    def get_bar(self, bar_name):
        bar_cursor = self.connection.cursor()
        bar_data = bar_cursor.execute("SELECT * FROM element_bar WHERE _id = ?",[bar_name]).fetchone()
        bar_data = list(bar_data)

        node_curser = self.connection.cursor()
        
        id = bar_data[0]
        node_a = self.get_node(bar_data[1])
        node_b = self.get_node(bar_data[2])
        section = self.get_section(bar_data[3])
        
        orientation_vector = str.replace(bar_data[4],'[','')
        orientation_vector = str.replace(orientation_vector,']','')
        orientation_vector = str.split(orientation_vector,' ')
        
        orientation_vector = np.array([float(orientation_vector[0]),
                                       float(orientation_vector[1]),
                                       float(orientation_vector[2])]
                                       )

        

        release_a = bar_data[5]
        release_b = bar_data[6]

        bar_object = element.Bar(node_a,
                                 node_b,
                                 section,
                                 orientation_vector,
                                 release_a, 
                                 release_b,
                                 id)
        
        return bar_object



 
    def close_connection(self):
        """
        Closes the connection to the model database. 
        IMPORTANT: this must be run to end work on the model.
        """

        self.connection.close()
        print( f'Connection to {self.database_path} closed')



class Results:
    def __init__(self):
        print('WIP')