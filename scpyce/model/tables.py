import sqlite3

def build_bar_table(connection):
    """
    Builds the bar table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

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
    cur.execute(bar_table_schema)

    cur.close()

def build_node_table(connection):
    """
    Builds the node table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
    node_table_schema = """
        CREATE TABLE IF NOT EXISTS element_node (
            _id INTEGER NOT NULL,
            x FLOAT NOT NULL,
            y FLOAT NOT NULL,
            z FLOAT NOT NULL
        );
        """
    cur.execute(node_table_schema)

    cur.close()

def build_support_table(connection):
    """
    Builds the support table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
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
    cur.execute(support_table_schema)

    cur.close()

def build_point_load_table(connection):
    """
    Builds the point load table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
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
    cur.execute(point_load_table_schema)

    cur.close()

def build_section_table(connection):
    """
    Builds the section table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
    section_table_schema = """
        CREATE TABLE IF NOT EXISTS property_section (
            _id TEXT PRIMARY KEY,
            material TEXT NOT NULL,
            area FLOAT NOT NULL,
            izz FLOAT NOT NULL,
            iyy FLOAT NOT NULL
        );
        """
    cur.execute(section_table_schema)

    cur.close()

def build_material_table(connection):
    """
    Builds the material table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
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
    cur.execute(material_table_schema)

    cur.close()

def build_node_displacements_table(connection):
    """
    Builds the node displacements table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
    results_node_displacements = """ 
        CREATE TABLE IF NOT EXISTS result_node_displacement (
        node_index int NOT NULL,
        load_case string NOT NULL,
        ux float NOT NULL,
        uy float NOT NULL,
        uz float NOT NULL,
        rx float NOT NULL,
        ry float NOT NULL,
        rz float NOT NULL
        ); """
    
    cur.execute(results_node_displacements)

    cur.close()

def build_node_reactions_table(connection):
    """
    Builds the node displacements table for the model database.
    """
    # create a database cursor
    cur = connection.cursor()

    # create the database table if it doesn't exist
    results_node_reactions = """ CREATE TABLE IF NOT EXISTS 
        result_node_reactions (
        node_index int NOT NULL,
        load_case string NOT NULL,
        fx float NOT NULL,
        fy float NOT NULL,
        fz float NOT NULL,
        mx float NOT NULL,
        my float NOT NULL,
        mz float NOT NULL
        ); """
    
    cur.execute(results_node_reactions)

    cur.close()


        