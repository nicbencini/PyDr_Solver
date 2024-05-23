import time
import model as mdl
import model.element as el

#Sign convention

# Positive values represent upward forces
# Negative values represent downward forces

# Clockwise moments are positive moments
# Counter Clockwise moments are negative moments


input('Run solver?')

startTime = time.time()
print('Solver Initialized.....')

bar = el.bar(1,2,3,4)

print (bar.release_a)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))