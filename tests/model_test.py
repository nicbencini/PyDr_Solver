import time
import numpy as np
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/pydr_solver')

print(parent_dir)

def bar_test():

    from model import element
    from model import property

    startTime = time.time()
    print('Bar Test Initialized.....')

    node1 = element.node(0,0,0)
    node2 = element.node(0,0,1)
    section = property.section.default()
    orientation_vector = np.array([1,0,0])

    bar = element.bar(node1,node2,section,orientation_vector)

    print(f'Bar Node A: {bar.node_a.to_array()}')
    print(f'Bar Node B: {bar.node_b.to_array()}')
    print(f'Bar Section: {bar.section.name}')
    print(f'Bar Material: {bar.section.material.name}')
    print(f'Bar Orientation: {bar.orientation_vector}')
    print(f'Bar Release A: {bar.release_a}')
    print(f'Bar Release B: {bar.release_b}')

    executionTime = (time.time() - startTime)
    
    print('Bar Test success...\nExecution time in seconds: ' + str(executionTime))

bar_test()