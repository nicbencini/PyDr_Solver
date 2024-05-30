import time
import numpy as np
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/pydr_solver')

from model import element
from model import property


startTime = time.time()
print('Model Test Initialized.....')

node1 = element.node(0,0,0)
node2 = element.node(0,0,1)
section = property.section.default()
orientation_vector = np.array([1,0,0])

bar = element.bar(node1,node2,section,orientation_vector)

print (bar.release_a)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))