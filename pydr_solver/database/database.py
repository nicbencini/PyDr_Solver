import sqlite3

class model:
    def __init__(self , file_path , name):
        self.database_path = file_path  + name + '.db'
        self.connection = sqlite3.connect(self.database_path)

        print(f'Connected to {self.database_path}')

    def build_tables(self):
        # create a database cursor
        cur = self.connection.cursor()

        # create the database table if it doesn't exist
        bar_table_schema = """
        CREATE TABLE IF NOT EXISTS element_node (
            _id TEXT PRIMARY KEY,
            node_a INTEGER NOT NULL,
            node_b INTEGER NOT NULL,
            section TEXT NOT NULL,
            local_plane TEXT NOT NULL,
            release_a TEXT NOT NULL,
            release_b TEXT NOT NULL
        );
        """
        
        node_table_schema = """
        CREATE TABLE IF NOT EXISTS element_bar (
            _id TEXT PRIMARY KEY,
            node_index INTEGER NOT NULL,
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
        print('Bar table built...')

        cur.execute(node_table_schema)
        print('Node table built...')

        cur.execute(support_table_schema)
        print('Support table built...')

        cur.execute(point_load_table_schema)
        print('Pointload table built...')

        cur.execute(material_table_schema)
        print('Material table built...')

        cur.execute(material_table_schema)
        print('Material table built...')

        cur.execute(section_table_schema)
        print('Section table built...')

        cur.close()

    def add_bar(bar):
        print('test')
        

    def close_connection(self):
        self.connection.close()
        print(f'Connection closed')



structral_model = model('/home/nicbencini/', 'test')
structral_model.build_tables()
structral_model.close_connection()