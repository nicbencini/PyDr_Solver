import time

#Sign convention

# Positive values represent upward forces
# Negative values represent downward forces

# Clockwise moments are positive moments
# Counter Clockwise moments are negative moments


startTime = time.time()
print('Solver Initialized.....')

input('Run solver?')

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))