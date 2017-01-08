import math
import random
print '20'
for i in range(0, 99, 5):
    print str(i) + ' ' + str(int(math.floor(random.random() * 100))) + ' ' + str(int(math.floor(random.random() * 100)))
