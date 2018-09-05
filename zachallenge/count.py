import sys
import os
fname = sys.argv[1]
res = None
with open(os.path.join(os.path.dirname(__file__), 'results', 'public_test_gt.csv'), 'r') as f:
    res = f.readlines()

content = None
with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
    content = f.readlines()
c = 0
# w = False 
for i, l in enumerate(content):
    x = l.split(',')
    x2 = ','.join([x[0].split('.')[0], x[1], x[2]])
    if not x2 == res[i]:
        c+=1

print ('wrong cases ', c)

print ('accu = ', (5559 - c)/ 5559 * 100, ' %')