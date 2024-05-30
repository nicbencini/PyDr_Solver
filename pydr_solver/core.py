import time
import numpy as np

from model import element
from model import property

#Sign convention

# Positive values represent upward forces
# Negative values represent downward forces

# Clockwise moments are positive moments
# Counter Clockwise moments are negative moments


#input('Run solver?')

startTime = time.time()
print('Solver Initialized.....')

node1 = element.node(0,0,0)
node2 = element.node(0,0,1)
section = property.section.default()
orientation_vector = np.array([1,0,0])

bar = element.bar(node1,node2,section,orientation_vector)

print (bar.release_a)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))