import time
import numpy as np

from objects import element
from scpyce.objects import properties

#Sign convention

# Positive values represent upward forces
# Negative values represent downward forces

# Clockwise moments are positive moments
# Counter Clockwise moments are negative moments


#input('Run solver?')

startTime = time.time()
print('Solver Initialized.....')



executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))