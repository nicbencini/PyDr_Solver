import time
import numpy as np
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/scpyce')

print(parent_dir)

def bar_test():

    from objects import element
    from objects import property

    startTime = time.time()
    print('Bar Test Initialized.....')

    node1 = element.Node(0,0,0)
    node2 = element.Node(0,0,1)
    section = property.Section.default()
    orientation_vector = np.array([1,0,0])

    bar = element.Bar(node1,node2,section,orientation_vector)

    print(f'Bar Id: {bar.id}')
    print(f'Bar Node A: {bar.node_a}')
    print(f'Bar Node B: {bar.node_b}')
    print(f'Bar Section: {bar.section.name}')
    print(f'Bar Material: {bar.section.material.name}')
    print(f'Bar Orientation: {bar.orientation_vector}')
    print(f'Bar Release A: {bar.release_a}')
    print(f'Bar Release B: {bar.release_b}')

    executionTime = (time.time() - startTime)
    
    print('Bar Test success...\nExecution time in seconds: ' + str(executionTime))

def pyramid_test():

    startTime = time.time()
    print('pyramid Test Initialized.....')

    from data import database
    from objects import element
    from objects import property
    from objects import load
    from engine import stiffness_matrix

    node1 = element.Node(1,1,2)
    node2 = element.Node(2,0,0)
    node3 = element.Node(0,0,0)
    node4 = element.Node(2,2,0)
    node5 = element.Node(0,2,0)

    section = property.Section.default()
    orientation_vector = np.array([1,0,0])

    bar1 = element.Bar(node1,node2,section,orientation_vector)
    bar2 = element.Bar(node1,node3,section,orientation_vector)
    bar3 = element.Bar(node1,node4,section,orientation_vector)
    bar4 = element.Bar(node1,node5,section,orientation_vector)

    support1 = element.Support.pin(node2)
    support2 = element.Support.pin(node3)
    support3 = element.Support.pin(node4)
    support4 = element.Support.pin(node5)

    load1 = load.PointLoad(node1,0,0,10,0,0,0)

    structural_model = database.Model('/home/nicbencini/', 'test')
    structural_model.build_tables()


    structural_model.add_bar(bar1)
    structural_model.add_bar(bar2)
    structural_model.add_bar(bar3)
    structural_model.add_bar(bar4)

    structural_model.add_support(support1)
    structural_model.add_support(support2)
    structural_model.add_support(support3)
    structural_model.add_support(support4)

    structural_model.add_point_load(load1)

    sm = stiffness_matrix.GlobalStiffnessMatrix(structural_model)
    print(sm.ndof_primary)

    structural_model.close_connection()

    executionTime = (time.time() - startTime)
    print('Database Test success...\nExecution time in seconds: ' + str(executionTime))

#bar_test()
pyramid_test()